# SCL <scott@rerobots.net>
# 2018

bootstrap:
	tar -c bootstrap.sh etc | gzip > bootstrapit.tgz

deploy:
	python manage.py collectstatic --noinput
	tar -c acarbroker etc manage.py static_to_deploy | gzip > shipit.tgz
