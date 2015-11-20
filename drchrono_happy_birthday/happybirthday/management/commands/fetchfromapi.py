from django.conf import settings
from django.core.management import BaseCommand
from optparse import make_option
import os
import sys
from happybirthday.models import Doctor, Patient
import shutil
import requests
from datetime import datetime

def update_from_api():
    pass


def fetch_doctors(token):
    auth_token_str = "Bearer %s" % token
    headers = {
        "Authorization": auth_token_str,
        "Content-Type": "application/json"
    }
    r = requests.get(settings.DOCTOR_API_URL, headers=headers)
    if r.status_code == requests.codes.ok:
        j = r.json()
        return j['results']


def fetch_patients(token):
    auth_token_str = "Bearer %s" % token
    headers = {
        "Authorization": auth_token_str,
        "Content-Type": "application/json"
    }
    r = requests.get(settings.PATIENTS_API_URL, headers=headers)
    if r.status_code == requests.codes.ok:
        j = r.json()
        return j['results']


def save_doctors(list_of_doctors):
    pass


def save_patients(list_of_patients, doctor):
    for p in list_of_patients:
        print p
        dob = p['date_of_birth']
        d = datetime.strptime("1986-03-17", "%Y-%m-%d")
        
        patient_in_db = Patient(
            first_name=p['first_name'],
            last_name = p['last_name'],
            email_id = p['email'],
            date_of_birth = d.date(),
            doctor=doctor
        )
        patient_in_db.save()


def reset_from_api():
    doctors = Doctor.objects.all()
    for doctor in doctors:
        token_obj = doctor.access_tokens.all()
        if len(token_obj) > 0:
            user_token = None
            patients_token = None
            for t in token_obj:
                if t.scope == settings.PATIENTS_SCOPE:
                    patients_token = t.token
                if t.scope == settings.USER_SCOPE:
                    user_token = t.token
            if user_token:
                list_of_doctors = fetch_doctors(user_token)
            if patients_token:
                list_of_patients = fetch_patients(patients_token)
                save_patients(list_of_patients, doctor)

class Command(BaseCommand):
    args = '<update reset>'
    help = "Fetches all the data from drchrono API"

    usage_str = "./manage.py fetchfromapi -o <update or reset>"
    option_list = BaseCommand.option_list + (
        make_option('-o', dest='option', help="update or reset"),
    )

    def handle(self, *args, **options):
        if not options['option']:
            self.error("Option not provided. \n" + self.usage_str)

        if options['option'] == settings.OPTION_TO_UPDATE:
            update_from_api()
        else:
            reset_from_api()

    @staticmethod
    def error(message, code=1):
        print(message)
        sys.exit(code)
