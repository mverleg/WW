
from django.conf.urls import patterns, url
from opinions.views import add_translation_vote, add_translation_comment, delete_translation_comment


urlpatterns = (
	url(r'^vote/$', add_translation_vote, name = 'add_translation_vote'),
	url(r'^comment/$', add_translation_comment, name = 'add_translation_comment'),
	url(r'^uncomment/$', delete_translation_comment, name = 'delete_translation_comment'),
)


