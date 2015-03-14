
"""
	This file is like the index in a book: it shows which url will lead to which code.
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.template import add_to_builtins
from basics.search import search
from basics.views import home, about, choose_language
import learners.urls, lists.urls, opinions.urls, phrasebook.urls, study.urls


urlpatterns = patterns('',
	url(r'^$', home, name = 'home'),
	url(r'^about/$', about, name = 'about'),
	url(r'^search/$', search, name = 'search'),
	url(r'^learner/', include(learners.urls)),
	url(r'^list/', include(lists.urls)),
	url(r'^opinion/', include(opinions.urls)),
	url(r'^phrase/', include(phrasebook.urls)),
	url(r'^study/', include(study.urls)),
	url(r'^languages/$', choose_language, name = 'choose_languages'),
	url(r'^admin/', include(admin.site.urls)),
)


"""
	This is kind of a hack:
"""
add_to_builtins('basics.tags')
add_to_builtins('django.templatetags.i18n')


