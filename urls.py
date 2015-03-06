
"""
	This file is like the index in a book: it shows which url will lead to which code.
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from basics.views import home, about, search, choose_language
from lists.views import user_lists, all_lists, show_list
import learners.urls
from phrasebook.views import show_phrase


urlpatterns = patterns('',
	url(r'^$', home, name = 'home'),
	url(r'^about/$', about, name = 'about'),
	url(r'^search/$', search, name = 'search'),
	url(r'^learner/', include(learners.urls)),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^list/(?P<pk>\d+)-(?P<slug>[-\w]+)/$', show_list, name = 'show_list'),
	url(r'^list/(?P<pk>\d+)/$', show_list, name = 'show_list'),
	url(r'^list/my/$', user_lists, name = 'user_lists'),
	url(r'^list/all/$', all_lists, name = 'all_lists'),
	url(r'^list/$', lambda request: redirect(reverse('user_lists'))),
	url(r'^choose_language/$', choose_language, name = 'choose_language'),
	url(r'^phrase/(?P<pk>\d+)/$', show_phrase, name = 'show_phrase'),
)


