
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from study.views import study, stats


urlpatterns = patterns('',
	url(r'^learn/$', study, name = 'study'),
	url(r'^stats/$', stats, name = 'study'),
	url(r'^$', lambda request: redirect(reverse('user_lists'))),
)


