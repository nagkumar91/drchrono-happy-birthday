from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel


class Doctor(AbstractUser):
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'


class Patient(TimeStampedModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_id = models.EmailField()
    date_of_birth = models.DateField(null=True)

    doctor = models.ForeignKey(Doctor, related_name='patients')

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


class AccessToken(models.Model):
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    doctor = models.ForeignKey(Doctor, related_name='access_tokens', null=True, blank=True)
    refresh_token = models.CharField(max_length=255)