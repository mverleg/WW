
"""
	This file is like the index in a book: it shows which url will lead to which code.
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from basics.views import home, about, search
import learners.urls


urlpatterns = patterns('',
	url(r'^$', home, name = 'home'),
	url(r'^about/$', about, name = 'about'),
	url(r'^search/$', search, name = 'search'),
	url(r'^learner/', include(learners.urls)),
	url(r'^admin/', include(admin.site.urls)),
)


