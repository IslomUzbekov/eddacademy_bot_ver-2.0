import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eddacademy.settings")

app = Celery("eddacademy")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
