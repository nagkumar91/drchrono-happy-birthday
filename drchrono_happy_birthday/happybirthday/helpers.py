import requests
from django.conf import settings
from .models import Doctor, Patient, AccessToken


def wish_happy_birthday(patient):
    doctor_name = "%s %s" % (patient.doctor.first_name, patient.doctor.last_name)
    from_name = "%s <%s>" % (doctor_name, patient.doctor.email)
    content = "Happy birthday from your doctor! -Dr. %s" % patient.doctor.email
    requests.post(
        settings.MAILGUN_API_URL,
        auth=("api", settings.MAILGUN_SECRET_KEY),
        data={"from": from_name,
              "to": [patient.email_id],
              "subject": "Happy birthday!",
              "text": content})


def get_doctor_info(code):
    redirect_url = "%s%s" % (settings.SITE_URL, settings.OAUTH_HANDLER_USER)
    data = {
        "client_id": settings.DRCHRONO_CLIENT_ID,
        "client_secret": settings.DRCHRONO_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_url,
        "code": code
    }
    r = requests.post(settings.CODE_TO_TOKEN_URL, data=data)
    access_token = None
    if r.status_code == requests.codes.ok:
        response = r.json()
        access_token = response['access_token']
    else:
        return None
    auth_token_str = "Bearer %s" % access_token
    headers = {
        "Authorization": auth_token_str,
        "Content-Type": "application/json"
    }
    d = None
    r = requests.get(settings.DOCTOR_API_URL, headers=headers)
    if r.status_code == requests.codes.ok:
        try:
            doctors = r.json()['results']
            for doctor in doctors:
                d, created = Doctor.objects.update_or_create(email=doctor['email'], defaults={
                    'first_name': doctor['first_name'],
                    'last_name': doctor['last_name'],
                    'username': doctor['email'],
                })
                d.save()
                d.send_email = True
                d.set_password(settings.DEFAULT_USER_PASSWORD)
                d.save()
                token, created = AccessToken.objects.update_or_create(doctor=d, defaults={
                    'user_token': code
                })
                token.save()
                return d
        except IndexError:
            print "indexeror"
    else:
        return None


def get_patients_info(code, doctor):
    redirect_url = "%s%s" % (settings.SITE_URL, settings.OAUTH_HANDLER_PATIENT)
    data = {
        "client_id": settings.DRCHRONO_CLIENT_ID,
        "client_secret": settings.DRCHRONO_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_url,
        "code": code
    }
    r = requests.post(settings.CODE_TO_TOKEN_URL, data=data)
    access_token = None
    if r.status_code == requests.codes.ok:
        response = r.json()
        access_token = response['access_token']
        token, created = AccessToken.objects.update_or_create(doctor=doctor, defaults={
            'patient': code
        })
        token.save()
    else:
        return None
    p_list = None
    auth_token_str = "Bearer %s" % access_token
    headers = {
        "Authorization": auth_token_str,
        "Content-Type": "application/json"
    }
    r = requests.get(settings.PATIENTS_API_URL, headers=headers)
    if r.status_code == requests.codes.ok:
        p_list = []
        try:
            patients = r.json()['results']
            for patient in patients:
                if patient['date_of_birth'] and patient['email']:
                    p = Patient(first_name=patient['first_name'], last_name=patient['last_name'],
                                date_of_birth=patient['date_of_birth'], doctor=doctor)
                    p.save()
                    p_list.append(p)
        except IndexError:
            print "indexeror"
    else:
        return None
    return len(p_list)
