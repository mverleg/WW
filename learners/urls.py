
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from learners.views import login, logout, register, password, profile


urlpatterns = patterns('',
	url(r'^$', lambda request: redirect(reverse('profile_actions')), name = 'profile'),
	url(r'^login/$', login, name = 'login'),
	url(r'^logout/$', logout, name = 'logout'),
	url(r'^register/$', register, name = 'register'),
	url(r'^password/$', password, name = 'password'),
	url(r'^profile/$', profile, name = 'profile'),
	#url(r'^settings/$', settings, name = 'settings'),
)


