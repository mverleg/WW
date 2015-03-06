
from django.shortcuts import render
from basics.views import notification
from basics.decorators import instantiate
from phrasebook.models import Phrase


@instantiate(Phrase, in_kw_name = 'pk', out_kw_name = 'phrase')
def show_phrase(request, phrase):
	return notification(request, 'No phrase view yet, sorry. %s' % phrase)


