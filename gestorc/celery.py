import os

from celery.schedules import crontab
from django.conf import settings

from celery import Celery

# integrando o celery com o django (indicando o módulo settings)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestorc.settings")
app = Celery("gestorc")

# permitindo o celery se auto configurar apartir das confs do settings django
app.config_from_object("django.conf:settings", namespace="CELERY")
# serve pra ele saber onde estão os módulos pra ele procurar por tarefas automaticamente

app.conf.beat_schedule = {
    "pending_invoices": {
        "task": "utils.tasks.check_pending_invoices",
        "schedule": crontab(minute=0, hour=7),
    },
}

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
