from django.contrib import admin

# Register your models here.
from .models import Doctor, Patient, AccessToken

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(AccessToken)
