from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drchrono_happy_birthday.settings.')

from django.conf import settings  # noqa
from .models import Doctor
from .helpers import wish_happy_birthday
import datetime
app = Celery('happybirthday')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self, *args, **kwargs):
    print "Processing the request"
    doctors = Doctor.objects.all()
    for doctor in doctors:
        patients = doctor.patients.all()

        for p in patients:
            if p.date_of_birth:
                if p.date_of_birth == datetime.date.today():
                    #wish birthday
                    wish_happy_birthday(p)
    print "Done!"