
from django.contrib.messages import add_message, INFO
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from basics.decorators import instantiate
from lists.models import ListAccess, PhraseList
from phrasebook.models import Translation


@instantiate(PhraseList, in_kw_name = 'pk', out_kw_name = 'phrase_list')
def show_list(request, phrase_list, slug = None, ListAccess=None):
	phrases = phrase_list.phrases.all()
	for phrase in phrases:
		phrase.lang_translations = Translation.objects.filter(language = request.lang, phrase = phrase)
	#todo: pagination (only load translations on page, for performance)
	return render(request, 'show_list.html', {
		'list': phrase_list,
		'phrases': phrases,
	})


def user_lists(request):
	if not request.user.is_authenticated():
		add_message(request, INFO, 'You can\'t manage your own lists yet. First register or login.')
		return redirect(reverse('all_lists'))
	edit_accesses = ListAccess.objects.filter(learner = request.user, access = ListAccess.EDIT)
	view_accesses = ListAccess.objects.filter(learner = request.user, access = ListAccess.VIEW)
	return render(request, 'user_lists.html', {
		'edit_accesses': edit_accesses,
		'view_accesses': view_accesses,
	})


def all_lists(request):
	#all_accesses = ListAccess.objects.filter(learner = request.user, access = ListAccess.EDIT)
	public_lists = PhraseList.objects.filter(public = True)
	return render(request, 'all_lists.html', {
		'public_lists': public_lists,
	})

