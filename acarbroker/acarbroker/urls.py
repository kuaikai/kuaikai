"""

SCL <scott@rerobots.net>
2018
"""
from __future__ import absolute_import

from django.conf import settings
from django.urls import path, include

from . import views


app_name = 'acarbroker'
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.aboutus, name='aboutus'),
    path('sim', views.simjobs, name='simjobs'),
    path('hwsim', views.hwsim_index, name='hwsim_index'),
    path('submit', views.submit, name='submit'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('complete/auth0', views.complete_auth0, name='complete_auth0'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
