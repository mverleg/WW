
from collections import OrderedDict
from datetime import timedelta
from django.contrib.messages import add_message, INFO
from django.shortcuts import render
from django.utils.timezone import datetime, now
from basics.views import notification
from learners.function import update_learner_actives, get_options, weighted_option_choice
from lists.models import ListAccess
from study.models import Result, ActiveTranslation


#class ListAccess(models.Model):
#	VIEW, EDIT = 'view', 'edit'
#	translations_list = models.ForeignKey(TranslationsList)
#	learner = models.ForeignKey(Learner)
#	access = models.CharField(choices = ((VIEW, 'view list'), (EDIT, 'edit list')), max_length = 4)
#	priority = models.SmallIntegerField(default = 0, help_text = 'Higher priority lists will show up more during learning sessions (only applies to you).')
#	active = models.BooleanField(default = False, help_text = 'Inactive lists don\'t show up during learning sessions (only applies to you).')


def study_ask(request):
	if request.user.is_authenticated():
		update_learner_actives(learner = request.user)
		#todo: active more cards
		options = get_options(request = request)
		if not options:
			return notification(request, 'You don\'t have enough phrases to start a quiz, sorry. You can add some active lists for more phrases!')
		if request.user.add_randomness:
			choice = weighted_option_choice(options)
		else:
			choice = options[0]
		asked = choice.translation
	else:
		add_message(request, INFO, 'You are studying anonymously. With an account, you can select phrases to learn and store your results!')
		return notification(request, 'anonymous study coming soon')
	known = asked.phrase

	return render(request, 'study_question.html', {
		'anonymous': True,

	})


def study_respond(request):
	return notification(request, 'No study yet!')
	request.user.phrase_index += 1 #save


def stats(request):
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
	active_translations = [active.translation for active in ActiveTranslation.objects.filter(learner = request.user)]
	#todo: possible_translations = [trans for trans in active_translations if trans.pk in all_translations_map.keys()]
	possible_translations = []

	return render(request, 'show_stats.html', {
		'summaries': summaries,
		'results_today': results_today,
		'all_lists': all_lists.count(),
		'active_lists': active_lists.count(),
		'all_translations': len(all_translations),
		'active_translations': len(active_translations),
		'possible_translations': len(possible_translations),
	})


