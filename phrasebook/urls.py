
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from phrasebook.views import show_phrase, add_phrase, edit_phrase, delete_phrase, add_translation, remove_translation


urlpatterns = patterns('',
	url(r'^show/(?P<pk>\d+)/$', show_phrase, name = 'show_phrase'),
	url(r'^create/$', add_phrase, name = 'add_phrase'),
	url(r'^edit/(?P<pk>\d+)/$', edit_phrase, name = 'edit_phrase'),
	url(r'^delete/$', delete_phrase, name = 'delete_phrase'),
	url(r'^add/$',add_translation, name = 'add_translation'),
	url(r'^remove/$', remove_translation, name = 'remove_translation'),
	#url(r'^$', lambda request: redirect(reverse('user_lists'))),
)


