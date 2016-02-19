
from django.conf.urls import url
from phrasebook.views import show_phrase, add_phrase, edit_phrase, delete_phrase, create_translation, delete_translation


urlpatterns = [
	url(r'^(?P<pk>\d+)/$', show_phrase, name = 'show_phrase'),
	url(r'^create/$', add_phrase, name = 'add_phrase'),
	url(r'^edit/(?P<pk>\d+)/$', edit_phrase, name = 'edit_phrase'),
	url(r'^delete/$', delete_phrase, name = 'delete_phrase'),
	url(r'^add/$', create_translation, name = 'create_translation'),
	url(r'^remove/$', delete_translation, name = 'delete_translation'),
	#url(r'^$', lambda request: redirect(reverse('user_lists'))),
]


