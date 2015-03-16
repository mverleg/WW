
from django.conf.urls import patterns, url
from study.views import study, stats, study_list_ask, study_list_respond, study_demo


urlpatterns = patterns('',
	url(r'^$', study, name = 'study_ask'),
	url(r'^$', study, name = 'study_respond'),
	url(r'^ask/(?P<pk>\d+)-(?P<slug>[-\w]+)/$', study_list_ask, name = 'study_list_ask'),
	url(r'^check/(?P<pk>\d+)-(?P<slug>[-\w]+)/$', study_list_respond, name = 'study_list_respond'),
	url(r'^stats/$', stats, name = 'stats'),
	url(r'^demo/$', study_demo, name = 'study_demo'),
)


