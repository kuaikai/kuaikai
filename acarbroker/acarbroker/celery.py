"""

SCL <scott@rerobots.net>
2018
"""
from __future__ import absolute_import

import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acarbroker.settings')

celery_app = Celery('acarbroker')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
