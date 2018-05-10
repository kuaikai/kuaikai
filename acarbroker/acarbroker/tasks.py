"""

SCL <scott@rerobots.net>
2018
"""
from __future__ import absolute_import

import base64
import json
import os
import os.path
import subprocess
import tarfile
import tempfile
import time

from celery import shared_task

from .models import SimJob


@shared_task(ignore_result=True)
def simjob(file_chunks, job_id):
    fd, path = tempfile.mkstemp()
    filename = os.path.basename(path)
    fp = os.fdopen(fd, 'wb')
    for chunk in file_chunks:
        fp.write(base64.b64decode(chunk))
    fp.close()
    del file_chunks
    container_name = None
    try:
        # Check that submission is tar file and has minimum set of files.
        tf = tarfile.open(name=path)
        for fname in ['build.sh', 'start.sh', 'stop.sh', 'post.sh']:
            tf.getmember(fname)
        tf.close()

        # Create Docker container for it
        container_name = 'simjob-{}'.format(job_id)
        subprocess.check_call(['docker', 'run', '-t', '-d', '--name', container_name, 'kuaikai/donkeycar-sim:latest'])
        subprocess.check_call(['docker', 'cp',
                               path, container_name + ':/root/'])
        os.unlink(path)
        path = None

        cp = subprocess.run(['docker', 'exec', container_name,
                             '/bin/tar', '-vxzf', '/root/' + filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True,
                            timeout=15)
        cp.check_returncode()

        cp = subprocess.run(['docker', 'exec', container_name,
                             '/root/build.sh'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True,
                            timeout=60)
        cp.check_returncode()

        cp = subprocess.run(['docker', 'exec', '-d', container_name,
                             '/root/start.sh'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True,
                            timeout=3)
        cp.check_returncode()

        trace_files = []
        action_taken = False
        start_time = time.time()
        while not action_taken and time.time() - start_time < 60:
            time.sleep(2)
            cp = subprocess.run(['docker', 'exec', container_name, 'bash', '-c', 'ls /tmp/kuaikai_sim_*'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
            if cp.returncode == 0 and len(cp.stdout.strip()) > 0:
                for name in cp.stdout.strip().split():
                    if name not in trace_files:
                        trace_files.append(name)
            for trace_file in trace_files:
                cp = subprocess.run(['docker', 'exec', container_name, 'tail', '-n', '1', trace_file],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    universal_newlines=True)
                cp.check_returncode()
                if len(cp.stdout) > 0:
                    try:
                        trace_item = json.loads(cp.stdout)
                        if 'fcn' in trace_item and trace_item['fcn'] == 'set_pwm':
                            action_taken = True
                    except:
                        pass

        # Mark sim job as done
        done = True
        if action_taken:
            result = 'OK'
        else:
            result = 'FAIL'
    except:
        done = True
        result = 'FAIL'
    finally:
        job = SimJob.objects.get(pk=job_id)
        job.done = done
        job.result = result
        job.save()
        if path is not None:
            os.unlink(path)
        if container_name is not None:
            cp = subprocess.run(['docker', 'rm', '-f', container_name])
