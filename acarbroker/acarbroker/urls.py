"""

SCL <scott@rerobots.net>
2018
"""
from __future__ import absolute_import

from django.conf import settings
from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.submit, name='submit'),
    path('signin', views.signin, name='signin'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
