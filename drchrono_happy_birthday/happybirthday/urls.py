from django.conf.urls import patterns, url, include

urlpatterns = patterns('happybirthday.views',
                       url(r'^oauth_handler_user/', 'oauth_handler_user'),
                       url(r'^oauth_handler_patient/', 'oauth_handler_patient'),
                       url(r'^home/', 'homepage'),
                       url(r'^opt_out/(?P<id>[\-\w]+)/$', 'opt_out'),
                       url(r'$^', 'home')
                       )