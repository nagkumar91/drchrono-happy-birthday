from background_task import background
from logging import getLogger
from .models import Doctor, Patient
logger = getLogger(__name__)
import datetime
from .helpers import wish_happy_birthday

@background(schedule=1)
def happy_birthday_task():
    print "in task"
    patients = Patient.objects.all()
    for p in patients:
        if p.date_of_birth == datetime.date.today():
            wish_happy_birthday(p)