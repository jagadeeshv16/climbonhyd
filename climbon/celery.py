from __future__ import absolute_import, unicode_literals 
import os 
from celery import Celery
# from celery import shared_task 

# Set default Django settings 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'climbon.settings') 
app = Celery('climbon')
# Celery will apply all configuration keys with defined namespace  
app.config_from_object('django.conf:settings', namespace='CELERY')   
# Load tasks from all registered apps 
app.autodiscover_tasks()