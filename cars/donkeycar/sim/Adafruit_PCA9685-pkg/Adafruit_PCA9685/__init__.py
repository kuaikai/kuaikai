"""

SCL <scott@rerobots.net>
2018
"""
import json
import os
import tempfile
import time


class PCA9685:
    def __init__(self):
        self._fd, self._pathname = tempfile.mkstemp(prefix='kuaikai_sim_', dir='/tmp', text=True)
        self._fp = os.fdopen(self._fd, 'wt')

    def __del__(self):
        self._fp.close()

    def set_pwm_freq(self, freq_hz):
        self._fp.write(json.dumps({
            'time': time.time(),
            'fcn': 'set_pwm_freq',
            'args': {'freq_hz': freq_hz},
        }) + '\n')

    def set_pwm(self, channel, on, off):
        self._fp.write(json.dumps({
            'time': time.time(),
            'fcn': 'set_pwm',
            'args': {'channel': channel, 'on': on, 'off': off},
        }) + '\n')
