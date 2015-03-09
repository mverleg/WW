
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from lists.views import show_list, user_lists, all_lists, add_list, edit_list


urlpatterns = patterns('',
	url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', show_list, name = 'show_list'),
	url(r'^(?P<pk>\d+)/$', show_list, name = 'show_list'),
	url(r'^my/$', user_lists, name = 'user_lists'),
	url(r'^all/$', all_lists, name = 'all_lists'),
	url(r'^add/$', add_list, name = 'add_list'),
	url(r'^edit/(?P<pk>\d+)-(?P<slug>[-\w]+)/$', edit_list, name = 'edit_list'),
	url(r'^edit/(?P<pk>\d+)/$', edit_list, name = 'edit_lists'),
	url(r'^$', lambda request: redirect(reverse('user_lists'))),
)


