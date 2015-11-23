from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
# Create your views here.
from django.template import RequestContext
from django.views.generic import ListView

from .models import Doctor, Patient
from .helpers import get_doctor_info, get_patients_info
from .tasks import send_opt_out_email


def oauth_handler_user(request):
    auth_token = request.GET.get("code", None)
    context_instance = RequestContext(request, {})
    if auth_token:
        doctor = get_doctor_info(auth_token)
        if doctor:
            doctor = authenticate(username=doctor.email, password=settings.DEFAULT_USER_PASSWORD)
            login(request, doctor)
            send_opt_out_email.delay(doctor)
            context_instance = RequestContext(request, {
                "doctor": doctor,
                "client_id": settings.DRCHRONO_CLIENT_ID,
                "scope": settings.PATIENTS_SCOPE,
                "redirect_url": "%s%s" % (settings.SITE_URL, settings.OAUTH_HANDLER_PATIENT)
            })
            return render_to_response("authenticated.html", context_instance)
        else:
            return render_to_response("error.html", context_instance)
    else:
        return render_to_response("error.html", context_instance)


@login_required
def oauth_handler_patient(request):
    print request
    code = request.GET.get("code", None)
    context_instance = RequestContext(request, {})
    if code or request.user:
        number_of_patients = get_patients_info(code, request.user)
        if number_of_patients or request.user:
            context_instance = RequestContext(request, {
                'number_of_patients': number_of_patients,
                'doctor': request.user
            })
            return render_to_response("done.html", context_instance)
        return render_to_response("error.html", context_instance)
    else:
        return render_to_response("error.html", context_instance)


@login_required
def homepage(request):
    print request.user
    context_instance = RequestContext(request, {
        'number_of_patients': None,
        'doctor': request.user
    })
    return render_to_response("done.html", context_instance)


def opt_out(request, id):
    d = Doctor.objects.get(pk=int(id))
    d.send_email = False
    d.save()
    return render_to_response("thank_you.html")


def home(request):
    if request.user.is_anonymous():
        context_instance = RequestContext(request, {
            "client_id": settings.DRCHRONO_CLIENT_ID,
            "scope": settings.USER_SCOPE,
            "redirect_url": "%s%s" % (settings.SITE_URL, settings.OAUTH_HANDLER_USER)
        })
        return render_to_response("home.html", context_instance)
    else:
        context_instance = RequestContext(request, {
            'number_of_patients': None,
            'doctor': request.user
        })
        return render_to_response("done.html", context_instance)


class PatientList(ListView):
    model = Patient
    template_name = 'patient_list.html'
    def get_queryset(self):
        return self.request.user.patients.all()
