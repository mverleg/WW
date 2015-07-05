
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from lists.views import show_list, user_lists, all_lists, add_list, edit_list, delete_list, follow_list, unfollow_list, \
	add_translation_by_search, add_translation_by_pk, remove_translation, list_followers, promote_follower, demote_follower


urlpatterns = patterns('',
	url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', show_list, name = 'show_list'),
	url(r'^(?P<pk>\d+)/$', show_list, name = 'show_list'),
	url(r'^my/$', user_lists, name = 'user_lists'),
	url(r'^all/$', all_lists, name = 'all_lists'),
	url(r'^add/$', add_list, name = 'add_list'),
	url(r'^edit/(?P<pk>\d+)-(?P<slug>[-\w]+)/$', edit_list, name = 'edit_list'),
	url(r'^edit/(?P<pk>\d+)/$', edit_list, name = 'edit_list'),
	url(r'^follow/(?P<pk>\d+)-(?P<slug>[-\w]+)/$', list_followers, name = 'list_followers'),
	url(r'^follow/(?P<pk>\d+)/$', list_followers, name = 'list_followers'),
	url(r'^demote/$', demote_follower, name = 'demote_follower'),
	url(r'^promote/$', promote_follower, name = 'promote_follower'),
	url(r'^delete/$', delete_list, name = 'delete_list'),
	url(r'^follow/$', follow_list, name = 'follow_list'),
	url(r'^unfollow/$', unfollow_list, name = 'unfollow_list'),
	url(r'^insert/search/$', add_translation_by_search, name ='insert_translation_search'),
	url(r'^insert/(?P<pk>\d+)/$', add_translation_by_pk, name = 'insert_translation_pk'),
	url(r'^remove/$', remove_translation, name = 'remove_translation'),
	url(r'^$', lambda request: redirect(reverse('user_lists'))),
)


