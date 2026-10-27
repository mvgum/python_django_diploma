import os
from celery import Celery

# Устанавливаем настройки Django по умолчанию для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Читаем настройки из settings.py (все переменные, начинающиеся на CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи в файлах tasks.py всех приложений
app.autodiscover_tasks()
