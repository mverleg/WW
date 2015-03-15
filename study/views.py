
from collections import OrderedDict
from datetime import timedelta
from django.shortcuts import render
from django.utils.timezone import datetime, now
from basics.views import notification
from lists.models import TranslationsList, ListAccess
from phrasebook.models import Translation
from study.models import Result, ActiveTranslation



#class ListAccess(models.Model):
#	VIEW, EDIT = 'view', 'edit'
#	translations_list = models.ForeignKey(TranslationsList)
#	learner = models.ForeignKey(Learner)
#	access = models.CharField(choices = ((VIEW, 'view list'), (EDIT, 'edit list')), max_length = 4)
#	priority = models.SmallIntegerField(default = 0, help_text = 'Higher priority lists will show up more during learning sessions (only applies to you).')
#	active = models.BooleanField(default = False, help_text = 'Inactive lists don\'t show up during learning sessions (only applies to you).')


def study_ask(request):
	#todo: make sure phrases aren't repeated too often in a row, especially if correct
	#todo: make the frequency depend on (recent) results
	#todo: make sure the user can't just hit F5 several times to get multiple results
	#todo: more generally, make sure the user can't manipulate the data, e.g. request specific phrases
	#active_list_access = ListAccess.object.filter()
	pass


def study_respond(request):
	return notification(request, 'No study yet!')


def stats(request):
	today_start = datetime(year = now().year, month = now().month, day = now().day)
	week_start = today_start - timedelta(days = now().weekday())
	month_start = datetime(year = now().year, month = now().month, day = 1)
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


