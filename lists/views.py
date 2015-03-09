from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, INFO
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from basics.decorators import instantiate
from lists.forms import ListForm
from lists.models import ListAccess, TranslationsList
from phrasebook.models import Translation


@instantiate(TranslationsList, in_kw_name = 'pk', out_kw_name = 'translation_list')
def show_list(request, translation_list, slug = None):
	phrases = translation_list.phrases.all()
	for phrase in phrases:
		phrase.lang_translations = Translation.objects.filter(language = request.LEARN_LANG, phrase = phrase)
	#todo: pagination (only load translations on page, for performance)
	return render(request, 'show_list.html', {
		'list': translation_list,
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
	public_lists = TranslationsList.objects.filter(public = True)
	return render(request, 'all_lists.html', {
		'public_lists': public_lists,
	})


@login_required
def add_list(request):
	form = ListForm(request.POST or None)
	if form.is_valid():
		""" Create the list and grant the user edit access """
		li = form.save()
		ListAccess(translation_list = li, learner = request.user, access = ListAccess.EDIT).save()
	return render(request, 'edit_list.html', {
		'form': form,
		'add': True,
	})


@login_required
@instantiate(TranslationsList, in_kw_name = 'pk', out_kw_name = 'translation_list')
def edit_list(request, translation_list, slug = None):
	form = ListForm(request.POST or None, instance = translation_list)
	if form.is_valid():
		form.save()
		return redirect(reverse('show_list', kwargs = {'pk': translation_list.pk, 'slug': translation_list.slug}))
	return render(request, 'edit_list.html', {
		'form': form,
		'add': False,
	})


