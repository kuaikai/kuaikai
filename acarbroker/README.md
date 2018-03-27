# Introduction

The autonomous car broker (*acarbroker*) is a Web server that receives
controller software from users and evaluates it in several settings, beginning
with pure simulation. If the controller passes all tests, then it is applied to
a robot car on a physical racetrack.

# Deployment

There is a bootstrap script that should be sufficient to obtain all required
dependencies and to create a system configuration that is ready for
deployment. The reference platform for it is Ubuntu 16.04, but any modern
Debian-derived (`apt` package management) GNU/Linux distribution should work.

# Development

While developing, you do not need to satisfy all of the requirements for
deployment. It should suffice to install the following:

* Django <https://djangoproject.com/>
* Celery <http://celeryproject.org/>
* LXD <https://linuxcontainers.org/lxd/>

At the time of writing, Django database migrations are not committed to the
repository. So, to begin, try

    python manage.py makemigrations
    python manage.py migrate

If applied to a blank database, then a user must be created. Try

    python manage.py createsuperuser

Then, enter each of the following commands in its own terminal:

    ./local-staging.sh
    celery worker -A acarbroker -l info
    python manage.py runserver

Open <http://127.0.0.1:8000/> in your Web browser, sign-in, and begin to upload!
