
from django.conf.urls import patterns, url
from importing.views import import_hackingchinese_radicals


urlpatterns = patterns('',
	url(r'^hackingchinese/radicals/$', import_hackingchinese_radicals, name = 'import_hackingchinese_radicals'),
)


