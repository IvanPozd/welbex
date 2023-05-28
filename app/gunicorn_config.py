command = '/home/ivo_pozdeev/Projects/web_dev/django-on-docker/app/env/bin/gunicorn'
pythonpath = '/home/ivo_pozdeev/Projects/web_dev/django-on-docker/app'
bind = '0.0.0.0:8000'
workers = 5
user = 'ivo_pozdeev'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=backend.settings'