
from collections import OrderedDict
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, INFO, ERROR
from django.core.urlresolvers import reverse
from django.forms import HiddenInput
from django.shortcuts import render, redirect
from django.utils.timezone import datetime, now
from basics.views import notification
from basics.decorators import instantiate
from study.function import update_learner_actives, add_more_active_phrases, get_current_question
from lists.models import ListAccess, TranslationsList
from study.forms import SolutionForm
from study.models import Result, ActiveTranslation


@login_required
def study_ask(request):
	#learn_translation = models.ForeignKey('study.ActiveTranslation', blank = True, null = True, default = None, related_name = 'current_learners')
	#is_revealed = models.BooleanField(default = False)
	if request.user.is_revealed:
		pass
	else:
		""" A lot of preparatory stuff. """
		msgs = []
		add_more_active_phrases(learner = request.user, msgs = msgs)
		update_learner_actives(learner = request.user)
		hidden, shown, msgs = get_current_question(learner = request.user, known_language = request.KNOWN_LANG, learn_language = request.LEARN_LANG)
		for lvl, txt in msgs:
			add_message(request, lvl, txt)
		request.user.learn_translation = None # whichever one is in the known language
		form = SolutionForm(None, initial = {'shown': shown})
		return render(request, 'study_question.html', {
			'anonymous': True,
			'shown': shown,
			'hidden_language': hidden.language_disp(),
			'form': form,
		})


def study_respond(request):
	#todo: check all translations in phrase in target language, not just a random one
	result_form = SolutionForm(request.POST)
	if not result_form.is_valid():
		add_message(request, ERROR, 'Could not find or understand the answer, sorry. Sending back to question page.')
		return redirect(reverse('study_ask'))
	hidden, shown, msgs = get_current_question(learner = request.user, known_language = request.KNOWN_LANG, learn_language = request.LEARN_LANG)
	if not shown == result_form.cleaned_data['shown']:
		add_message(request, ERROR, 'Sorry, the active phrase has changed while you answered this question, so no statistics will be recorded. Possibly someone changed a list or you changed the language?')
		return redirect(reverse('study_ask'))
	correct = False
	if result_form.cleaned_data['solution'] == hidden.text:
		Result(learner = request.user, asked = hidden, known = shown, result = Result.CORRECT, verified = True).save()
		correct = True
	result_form.fields['solution'].widget = HiddenInput()
	#request.user.phrase_index += 1 #save
	#request.user.save() # todo: enable
	#todo: set it to wrong, then let the user click something to mark correct/incorrect?
	#todo: better save the card on the user after all; target_translation and is_revealed
	return render(request, 'study_result.html', {
		'hidden': hidden,
		'shown': shown,
		'correct': correct,
		'result_form': result_form,
		'answer': result_form.cleaned_data['solution'].strip(),
	})


@instantiate(TranslationsList, in_kw_name = 'pk', out_kw_name = 'translations_list')
def study_list_ask(request, translations_list, slug):
	add_message(request, INFO, 'You are studying anonymously. With an account, you can select phrases to learn and store your results!')
	return notification(request, 'Anonymous study coming soon')
	#todo: anonymous study should study a specific list


@instantiate(TranslationsList, in_kw_name = 'pk', out_kw_name = 'translations_list')
def study_list_respond(request, translations_list, slug):
	pass


def study_demo(request):
	"""
		Redirect to a list to study (the first public one).
	"""
	lis = TranslationsList.objects.filter(public = True).order_by('pk')
	if not lis:
		return notification('There is no public list to study, sorry...')
	return redirect(reverse('study_list_ask', kwargs = {'pk': lis[0].pk, 'slug': lis[0].slug}))


@login_required
def stats(request):
	#todo: stats per language
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
	results_today = Result.objects.filter(learner = request.user, when__gt = now() - timedelta(days = 1))
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


