import requests
from django.conf import settings


def wish_happy_birthday(patient):
    doctor_name = "%s %s" % (patient.doctor.first_name, patient.doctor.last_name)
    from_name = "%s <%s>" % (doctor_name, patient.doctor.email)
    content = "Happy birthday from your doctor! -Dr. %s" % patient.doctor.email
    print "sending mail to %s" % patient
    requests.post(
        settings.MAILGUN_API_URL,
        auth=("api", settings.MAILGUN_SECRET_KEY),
        data={"from": from_name,
              "to": [patient.email_id],
              "subject": "Happy birthday!",
              "text": content})
