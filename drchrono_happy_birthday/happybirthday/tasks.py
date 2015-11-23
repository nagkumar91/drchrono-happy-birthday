from __future__ import absolute_import
import os

import requests
from celery import Celery, shared_task
# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drchrono_happy_birthday.settings.')

from django.conf import settings  # noqa
from .models import Doctor, Patient
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
            if p.date_of_birth and p.email_id:
                if p.date_of_birth == datetime.date.today():
                    # wish birthday
                    wish_happy_birthday(p)
    print "Done!"


@shared_task
def send_opt_out_email(doctor, *args, **kwargs):
    content = "You have chosen opt out. Please click on the link below to confirm. %s/opt_out/%s/" % (
        settings.SITE_URL, doctor.pk)
    requests.post(
        settings.MAILGUN_API_URL,
        auth=("api", settings.MAILGUN_SECRET_KEY),
        data={"from": "happybirthdayapp@happybirthdayapp.com",
              "to": [doctor.email],
              "subject": "Opt out!",
              "text": content})


@shared_task
def refresh_token(token):
    return None


@shared_task
def get_new_patients(doctor, token):
    auth_token_str = "Bearer %s" % token
    headers = {
        "Authorization": auth_token_str,
        "Content-Type": "application/json"
    }
    r = requests.get(settings.PATIENTS_API_URL, headers=headers)
    if r.status_code == requests.codes.ok:
        patients = r.json()['results']
        for p in patients:
            # if p['date_of_birth'] and p['email']:
            p, created = Patient.objects.update_or_create(pk=p['id'], defaults={
                "first_name": p['first_name'],
                "last_name": p['last_name'],
                "date_of_birth": p['date_of_birth'],
                "doctor": doctor
            })
            p.save()


@app.task(bind=True)
def update_records(self, *args, **kwargs):
    doctors = Doctor.objects.all()
    for doctor in doctors:
        tokens = doctor.access_tokens.all()
        for token in tokens:
            new_token = refresh_token(token)
            if new_token:
                token.patient_token = new_token['patient_token']
                token.user_token = new_token['user_token']
                token.save()
        get_new_patients(doctor, tokens[0].patient_token)
