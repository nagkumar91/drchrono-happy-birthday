from __future__ import absolute_import
import os

import requests
from celery import Celery, shared_task
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
                    # wish birthday
                    wish_happy_birthday(p)
    print "Done!"


@shared_task
def send_opt_out_email(doctor, *args, **kwargs):
    content = "You have chosen opt out. Please click on the link below to confirm. %s/opt_out/%s" % (
    settings.SITE_URL, doctor.pk)
    requests.post(
        settings.MAILGUN_API_URL,
        auth=("api", settings.MAILGUN_SECRET_KEY),
        data={"from": "happybirthdayapp@happybirthdayapp.com",
              "to": [doctor.email],
              "subject": "Opt out!",
              "text": content})
