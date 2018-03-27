"""

SCL <scott@rerobots.net>
2018
"""
from __future__ import absolute_import

from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),
]
