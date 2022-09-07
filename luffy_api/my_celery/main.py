from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "luffy_api.settings.dev")
import django
django.setup()

app = Celery("luffy")
app.config_from_object("luffy_api.my_celery.config")
app.autodiscover_tasks(["luffy_api.my_celery.sms"])