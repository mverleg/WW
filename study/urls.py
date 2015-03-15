
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from study.views import study_ask, study_respond, stats


urlpatterns = patterns('',
	url(r'^ask/$', study_ask, name = 'study_ask'),
	url(r'^check/$', study_respond, name = 'study_respond'),
	url(r'^stats/$', stats, name = 'stats'),
	url(r'^$', lambda request: redirect(reverse('study_ask')), name = 'study'),
)


