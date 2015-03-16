
from django.conf.urls import patterns, url
from study.views import study_ask, study_respond, stats, study_list_ask, study_list_respond, study_demo


urlpatterns = patterns('',
	url(r'^ask/$', study_ask, name = 'study_ask'),
	url(r'^check/$', study_respond, name = 'study_respond'),
	url(r'^ask/(?P<pk>\d+)-(?P<slug>[-\w]+)/$', study_list_ask, name = 'study_list_ask'),
	url(r'^check/(?P<pk>\d+)-(?P<slug>[-\w]+)/$', study_list_respond, name = 'study_list_respond'),
	url(r'^stats/$', stats, name = 'stats'),
	url(r'^$', study_demo, name = 'study_demo'),
)


