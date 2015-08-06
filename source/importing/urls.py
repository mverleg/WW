
from django.conf.urls import patterns, url
from importing.views import import_hackingchinese_radicals, import_chinesepod_dialogue


urlpatterns = patterns('',
	url(r'^hackingchinese/radicals/$', import_hackingchinese_radicals, name = 'import_hackingchinese_radicals'),
	url(r'^chinesepod/$', import_chinesepod_dialogue, name = 'import_chinesepod_dialogue'),
)


