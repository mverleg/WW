
from collections import OrderedDict
from datetime import timedelta
from random import shuffle, random
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, INFO, ERROR
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.timezone import datetime, now
from basics.views import notification
from basics.decorators import instantiate
from learners.models import Learner
from study.function import update_learner_actives, add_more_active_phrases, get_current_question
from lists.models import ListAccess, TranslationsList
from study.forms import SolutionForm, AnonStudyForm
from study.models import Result, ActiveTranslation
from study.score import update_score


@login_required
def study(request):
	#todo: show the last X results while studying (easy with Result)
	learner = request.user
	result_form = SolutionForm(request.POST)
	if learner.study_state == Learner.ASKING and 'solution' in request.POST:
		"""
			The user submitted a solution.
		"""
		if not result_form.is_valid():
			add_message(request, ERROR, 'Could not find or understand the answer, sorry. Sending back to question.')
			return redirect(reverse('study_ask'))
		learner.study_answer = result_form.cleaned_data['solution'].strip()
		if learner.study_answer == learner.study_hidden.text.strip():
			#todo: also check other languages in the future maybe
			""" Update the score (so it can be set to 'verified') but only go on to next card when user click 'go on'. """
			update_score(learner, Result.CORRECT, verified=True)
			learner.study_state = Learner.JUDGED
		else:
			learner.study_state = Learner.REVEALED
		learner.save()
	if learner.study_state in [Learner.REVEALED, Learner.JUDGED] and 'result' in request.POST:
		"""
			The user judged the result, process it and go to the next question.
		"""
		result_map = {'correct': Result.CORRECT, 'notquite': Result.CLOSE, 'incorrect': Result.INCORRECT}
		try:
			result = result_map[request.POST['result']]
		except KeyError:
			return notification(request, 'The result you submitted, "%s", was not of expected format.' % request.POST['result'])
		if learner.study_state == Learner.REVEALED:
			update_score(learner, result)
		learner.study_shown = learner.study_hidden = None
		learner.study_answer = ''
		learner.phrase_index += 1
		learner.study_state = Learner.ASKING
		learner.save()
		""" Skip the judged page; set to asking and match later. """
	if learner.study_state in [Learner.REVEALED, Learner.JUDGED]:
		"""
			Show the solution.
		"""
		correct = learner.study_answer == learner.study_hidden.text.strip()
		judge = False if correct else learner.study_state == Learner.REVEALED
		return render(request, 'study_result.html', {
			'hidden': learner.study_hidden,
			'shown': learner.study_shown,
			'correct': correct,
			'judge': judge,
			'answer': learner.study_answer,
			'result_form': result_form,
			'list': None,
		})
	if learner.study_state == Learner.NOTHING:
		learner.study_state = Learner.ASKING
		learner.save()
	if learner.study_state == Learner.ASKING:
		"""
			Since there's no solution in POST, the user just wants to see the question.
		"""
		msgs = []
		if not learner.study_shown or not learner.study_hidden:
			add_more_active_phrases(learner = learner, lang = request.LEARN_LANG, msgs = msgs)
			update_learner_actives(learner = learner)
			learner.study_hidden, learner.study_shown, msgs = get_current_question(learner = learner, known_language = request.KNOWN_LANG, learn_language = request.LEARN_LANG)
			learner.save()
		for lvl, txt in msgs:
			add_message(request, lvl, txt)
		form = SolutionForm(None)
		return render(request, 'study_question.html', {
			'shown': learner.study_shown,
			'hidden_language': learner.study_hidden.language_disp(),
			'form': form,
			'list': None,
		})
	raise Exception('nothing matched')


@instantiate(TranslationsList, in_kw_name = 'pk', out_kw_name = 'translations_list')
def study_list_ask(request, translations_list, slug):
	"""
		Study a single list, mostly for demonstration purposes (so no account is needed). Doesn't save results,
		doesn't store state and easy to cheat with.
	"""
	translations = list(translations_list.translations.all()[:500])
	shuffle(translations)
	for translation in translations:
		if translation.language == request.KNOWN_LANG:
			correct_lang_trans = translation.phrase.translations.filter(language = request.LEARN_LANG)
		elif translation.language == request.LEARN_LANG:
			correct_lang_trans = translation.phrase.translations.filter(language = request.KNOWN_LANG)
		else:
			continue
		""" Find a translation of this one that is in the correct langauge """
		if not correct_lang_trans:
			continue
		shown, hidden = translation, correct_lang_trans[0]
		if random() > 0.5:
			shown, hidden = hidden, shown
		form = AnonStudyForm(None, initial = {
			'shown': shown,
			'hidden': hidden,
		})
		return render(request, 'study_question.html', {
			'shown': shown,
			'hidden_language': hidden.language_disp(),
			'form': form,
			'list': translations_list,
		})
	return notification(request, 'The list seems to contain no pairs of phrases in the languages you know and study.')


@instantiate(TranslationsList, in_kw_name = 'pk', out_kw_name = 'translations_list')
def study_list_respond(request, translations_list, slug):
	if not request.POST:
		add_message(request, INFO, 'No answer detected, sending back to a new question.')
		return redirect(reverse('study_list_ask', kwargs = {'pk': translations_list.pk, 'slug': translations_list.slug}))
	form = AnonStudyForm(request.POST)
	if form.is_valid():
		shown, hidden, answer = form.cleaned_data['shown'], form.cleaned_data['hidden'], form.cleaned_data['solution'].strip()
		correct = answer == hidden.text.strip()
		judge = not correct
		result_form = SolutionForm(request.POST)
		return render(request, 'study_result.html', {
			'hidden': hidden,
			'shown': shown,
			'correct': correct,
			'judge': judge,
			'answer': answer,
			'result_form': result_form,
			'list': translations_list,
		})


def study_demo(request):
	"""
		Redirect to a list to study (the first public one).
	"""
	lis = TranslationsList.objects.filter(public = True).order_by('pk')
	if not lis:
		return notification(request, 'There is no public list to study, sorry...')
	return redirect(reverse('study_list_ask', kwargs = {'pk': lis[0].pk, 'slug': lis[0].slug}))


@login_required
def stats(request):
	#todo: stats per language
	#todo: bar plot of stats per day
	update_learner_actives(learner = request.user)
	today_start = datetime(year = now().year, month = now().month, day = now().day, tzinfo = now().tzinfo)
	week_start = today_start - timedelta(days = now().weekday())
	month_start = datetime(year = now().year, month = now().month, day = 1, tzinfo = now().tzinfo)
	summaries = OrderedDict((
		('today', {
			'correct': Result.objects.filter(learner = request.user, when__gt = today_start, result = Result.CORRECT).count(),
			'total': Result.objects.filter(learner = request.user, when__gt = today_start).count(),
		}),
		('this week', {
			'correct': Result.objects.filter(learner = request.user, when__gt = week_start, result = Result.CORRECT).count(),
			'total': Result.objects.filter(learner = request.user, when__gt = week_start).count(),
		}),
		('this month', {
			'correct': Result.objects.filter(learner = request.user, when__gt = month_start, result = Result.CORRECT).count(),
			'total': Result.objects.filter(learner = request.user, when__gt = month_start).count(),
		}),
		('all time', {
			'correct': Result.objects.filter(learner = request.user, when__gt = now(), result = Result.CORRECT).count(),
			'total': Result.objects.filter(learner = request.user, when__gt = now()).count(),
		}),
	))
	for label, data in summaries.items():
		summaries[label]['percentage'] = 100 * summaries[label]['correct'] / max(summaries[label]['total'], 1)
	results_today = Result.objects.filter(learner = request.user, when__gt = now() - timedelta(days = 1))[:100]
	all_lists = ListAccess.objects.filter(learner = request.user)
	active_lists = ListAccess.objects.filter(learner = request.user, active = True)
	all_translations_duplicates = sum([list(li.translations_list.translations.all()) for li in all_lists], [])
	all_translations_map = {trans.pk: trans for trans in all_translations_duplicates}
	all_translations = all_translations_map.values()
	active_translations = ActiveTranslation.objects.filter(learner = request.user)
	possible_translations = ActiveTranslation.objects.filter(learner = request.user, active = True)
	return render(request, 'show_stats.html', {
		'summaries': summaries,
		'results_today': results_today,
		'all_lists': all_lists.count(),
		'active_lists': active_lists.count(),
		'all_translations': len(all_translations),
		'active_translations': len(active_translations),
		'possible_translations': len(possible_translations),
	})


