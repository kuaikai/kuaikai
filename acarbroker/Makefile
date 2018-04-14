# SCL <scott@rerobots.net>
# 2018

deploy:
	python manage.py collectstatic --noinput
	tar -c acarbroker etc manage.py static_to_deploy | gzip > shipit.tgz
