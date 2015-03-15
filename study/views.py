
from collections import OrderedDict
from datetime import timedelta
from random import random
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, get_messages, INFO, ERROR
from django.shortcuts import render
from django.utils.timezone import datetime, now
from basics.views import notification
from learners.function import update_learner_actives, get_options, weighted_option_choice, add_more_active_phrases
from lists.models import ListAccess
from study.models import Result, ActiveTranslation


@login_required
def study_ask(request):
	""" A lot of preparatory stuff. """
	msgs = []
	add_more_active_phrases(learner = request.user, msgs = msgs)
	update_learner_actives(learner = request.user)
	options = get_options(learner = request.user, msgs = msgs, lang = request.LEARN_LANG)
	if not options:
		return notification(request, 'You don\'t have enough phrases to start a quiz, sorry. You can add some active lists for more phrases!')
	""" Choose among the options. """
	choice = options[0]
	if request.user.add_randomness:
		choice = weighted_option_choice(options)
	""" Now get the other language versions. """
	other_li = choice.translation.phrase.translations.filter(language = request.KNOWN_LANG)
	#todo: order shown_li by votes to get the best one
	if not other_li:
		other_li = choice.translation.phrase.translations.exclude(language = request.LEARN_LANG)
	if not other_li:
		""" There is only one translation so we don't know what to ask. Disable the bad card, try again (note that messages are intentionally lost). """
		add_message(request, ERROR, 'The phrase "%s" was skipped because there are no alternative language versions.' % choice.translation.text)
		choice.active = False
		choice.save()
		return study_ask(request)
	""" Choice.translation is in the unknown language; should we show this or ask for this? """
	#todo: store this somewhere, or the direction might change when the user reloads the page - possibly use the phrase_index as random seed or something
	if random() * 100 < request.user.ask_direction:
		""" We'll ask the learning language and show a (hopefully) known one. """
		hidden = choice.translation
		shown = other_li[0]
	else:
		hidden = other_li[0]
		shown = choice.translation
	for lvl, txt in msgs:
		add_message(request, lvl, txt)
	return render(request, 'study_question.html', {
		'anonymous': True,
		'shown': shown,
	})


def study_respond(request):
	return notification(request, 'No study yet!')
	request.user.phrase_index += 1 #save



def study_list_ask(request, translations_list):
	add_message(request, INFO, 'You are studying anonymously. With an account, you can select phrases to learn and store your results!')
	return notification(request, 'Anonymous study coming soon')
	#todo: anonymous study should study a specific list


def study_list_respond(request, translations_list):
	pass


def stats(request):
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


