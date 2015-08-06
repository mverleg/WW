
"""
	This file is like the index in a book: it shows which url will lead to which code.
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.template import add_to_builtins
from django.views.generic import TemplateView
from basics.search import search
from basics.views import choose_language
import learners.urls, lists.urls, opinions.urls, phrasebook.urls, study.urls, importing.urls


urlpatterns = patterns('',
	url(r'^$', TemplateView.as_view(template_name = 'home.html'), name = 'home'),
	url(r'^about/$', TemplateView.as_view(template_name = 'about.html'), name = 'about'),
	url(r'^about/study/$', TemplateView.as_view(template_name = 'about_study.html'), name = 'about_study'),
	url(r'^search/$', search, name = 'search'),
	url(r'^learner/', include(learners.urls)),
	url(r'^list/', include(lists.urls)),
	url(r'^opinion/', include(opinions.urls)),
	url(r'^phrase/', include(phrasebook.urls)),
	url(r'^study/', include(study.urls)),
	url(r'^import/', include(importing.urls)),
	url(r'^languages/$', choose_language, name = 'choose_languages'),
	url(r'^admin/', include(admin.site.urls)),
)


"""
	This is kind of a hack:
"""
add_to_builtins('basics.tags')
add_to_builtins('django.templatetags.i18n')


