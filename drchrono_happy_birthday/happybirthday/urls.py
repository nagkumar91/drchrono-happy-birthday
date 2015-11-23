from django.conf.urls import patterns, url, include

from .views import PatientList

urlpatterns = patterns('happybirthday.views',
                       url(r'^oauth_handler_user/', 'oauth_handler_user', name='oauth_handler_user'),
                       url(r'^oauth_handler_patient/', 'oauth_handler_patient', name='oauth_handler_patient'),
                       url(r'^home/', 'homepage', name='homepage'),
                       url(r'^patient_list/', PatientList.as_view(), name='patients_list'),
                       url(r'^add_patient/', 'add_patient', name='add_patient'),
                       url(r'^opt_out/(?P<id>[\-\w]+)/$', 'opt_out', name='opt_out'),
                       url(r'$^', 'home', name='home')
                       )