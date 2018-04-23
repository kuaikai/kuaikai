# SCL <scott@rerobots.net>
# 2018

bootstrap:
	tar -c bootstrap.sh etc | gzip > bootstrapit.tgz

deploy:
	python -c 'from acarbroker.settings import DEBUG; assert not DEBUG, "use DEBUG=False in production!"'
	python manage.py collectstatic --noinput
	tar -c acarbroker etc manage.py static_to_deploy | gzip > shipit.tgz
