
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, INFO, WARNING, ERROR
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from basics.decorators import instantiate, next_GET, confirm_delete
from basics.views import notification
from lists.models import TranslationsList
from phrasebook.forms import CreateTranslationForm, EditPhraseForm, PhraselessTranslationForm
from phrasebook.models import Phrase, Translation


@instantiate(Phrase, in_kw_name = 'pk', out_kw_name = 'phrase')
def show_phrase(request, phrase):
	#todo: there is of course room for improvement, e.g. show whether you have voted for an item, sort by number of votes and active language, ... These are not overly complicated but require some coding and queries (performance).
	#if not (phrase.public_view or phrase.learner == request.user):
	#	return notification(request, 'You don\'t have permission to view this phrase')
	try:
		translation_list = TranslationsList.objects.get(pk = int(request.GET['list']))
	except (TranslationsList.DoesNotExist, ValueError, KeyError):
		translation_list = None
	translations = Translation.objects.filter(phrase = phrase)
	learn_translations, known_translations, other_translations = [], [], []
	for translation in translations:
		if translation.language == request.KNOWN_LANG:
			known_translations.append(translation)
		elif translation.language == request.LEARN_LANG:
			learn_translations.append(translation)
		else:
			other_translations.append(translation)
	create_translation_form = CreateTranslationForm(None, initial = {'phrase': phrase, 'language': request.KNOWN_LANG})
	return render(request, 'show_phrase.html', {
		'phrase': phrase,
		'translations': translations,
		'create_translation_form': create_translation_form,
		'from_list': translation_list,
	})


def add_phrase(request):
	try:
		translation_list = TranslationsList.objects.get(pk = int(request.GET['list']))
	except (TranslationsList.DoesNotExist, ValueError, KeyError):
		translation_list = None
	phrase_form = EditPhraseForm(request.POST or None, initial = {'language': request.KNOWN_LANG})
	translation_form = PhraselessTranslationForm(request.POST or None, initial = {
		'language': translation_list.language if translation_list else None,
		'text': request.GET.get('phrase', ''),
	})
	if phrase_form.is_valid() and translation_form.is_valid():
		phrase = phrase_form.save(commit = False)
		phrase.learner = request.user
		phrase.save()
		translation = translation_form.save(commit = False)
		translation.phrase = phrase
		translation.save()
		if 'add_to_list' in request.POST and translation_list:
			translation_list.translations.add(translation)
			translation_list.save()
			return redirect('{0:s}?list={1:d}'.format(phrase_form.instance.get_absolute_url(), translation_list.pk))
		""" No need for translations update since a phrase with one translation is never valid for study. """
		return redirect(phrase_form.instance.get_absolute_url())
	return render(request, 'add_phrase.html', {
		'phrase_form': phrase_form,
		'translation_form': translation_form,
		'add_list': translation_list,
		'suggested_phrase': request.GET.get('phrase', ''),
	})


@login_required
@instantiate(Phrase, in_kw_name = 'pk', out_kw_name = 'phrase')
@next_GET
def edit_phrase(request, phrase, next = None):
	if not (phrase.public_edit or phrase.learner == request.user):
		return notification(request, 'You don\'t have permission to edit this phrase.')
	phrase_form = EditPhraseForm(request.POST or None, instance = phrase)
	if phrase_form.is_valid():
		phrase_form.save()
		""" No need for actives_update here, doesn't affect translations. """
		return redirect(request.POST['next'] or phrase.get_absolute_url())
	return render(request, 'edit_phrase.html', {
		'phrase': phrase,
		'phrase_form': phrase_form,
		'next': next,
	})


@require_POST
@login_required
@confirm_delete
def delete_phrase(request):
	try:
		phrase = Phrase.objects.get(pk = int(request.POST['pk']))
	except (KeyError, ValueError, Phrase.DoesNotExist):
		return notification(request, 'The phrase you were looking for was not found; the submitted data may be invalid.')
	if not (phrase.public_edit or phrase.learner == request.user):
		return notification(request, 'You don\'t have permission to delete this phrase.')
	phrase.delete()
	request.user.need_active_update = True
	request.user.save()
	return redirect(reverse('user_lists'))


@require_POST
@login_required
def create_translation(request):
	if not request.POST['language'].strip():
		add_message(request, ERROR, 'You need to provide the language for this phrase.')
		return redirect(request.POST['next'] or '/')
	form = CreateTranslationForm(request.POST)
	if form.is_valid():
		phrase = form.cleaned_data['phrase']
		if not (phrase.public_edit or phrase.learner == request.user):
			return notification(request, 'You don\'t have permission to add translations to this phrase.')
		if Translation.objects.filter(text = form.cleaned_data['text'], phrase = form.cleaned_data['phrase'], language = form.cleaned_data['language']):
			add_message(request, WARNING, 'This exact translation was already included and has been skipped.')
		else:
			add_message(request, INFO, 'Your translation "%s" has been added!' % form.cleaned_data['phrase'])
			form.save()
			request.user.need_active_update = True
			request.user.save()
		return redirect(request.POST['next'] or phrase.get_absolute_url())
	return notification(request, 'The submitted phrase was not valid, sorry. %s' % ' '.join('%s: %s' % (field, msg) for field, msg in list(form.errors.items())))


@require_POST
@login_required
def delete_translation(request):
	try:
		translation = Translation.objects.get(pk = int(request.POST['pk']))
	except (KeyError, ValueError, Translation.DoesNotExist):
		return notification(request, 'The translation you were looking for was not found; the submitted data may be invalid.')
	next = request.POST['next'] or translation.phrase.get_absolute_url()
	if translation.score >= 0 and not translation.phrase.learner == request.user:
		add_message(request, ERROR, 'You can only remove translations that have a negative vote score (unless you\'re the owner)')
	else:
		add_message(request, INFO, 'The translation has been deleted')
		translation.delete()
		request.user.need_active_update = True
		request.user.save()
	return redirect(next)


