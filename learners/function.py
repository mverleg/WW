
from random import random
from django.db.transaction import atomic
from lists.models import ListAccess
from study.models import Result, ActiveTranslation
from django.contrib.messages import add_message, WARNING


@atomic
def update_learner_actives(learner, force = False):
	"""
		If needed (or force is True), update all the learner's ActiveTranslation .priority and .active properties.
	"""
	if not (force or learner.need_active_update):
		return
	accesses = ListAccess.objects.filter(learner = learner, active = True)
	actives_map = {active.translation.pk: active for active in ActiveTranslation.objects.filter(learner = learner)}
	for pk, active in actives_map.items():
		active.active = False
		active.priority = 0
	for access in accesses:
		translations = access.translations_list.translations.all()
		for translation in translations:
			if not translation.pk in actives_map:
				continue
			active = actives_map[translation.pk]
			active.active = True
			if access.priority > active.priority:
				active.priority = access.priority
	for active in actives_map.values():
		active.save()
	learner.need_active_update = False
	learner.save()


def get_options(request, amount = 20):
	msg = None
	options = ActiveTranslation.objects.filter(
		learner = request.user,
		active = True,
		last_shown__lt = request.user.phrase_index - request.user.minimum_delay - (amount if request.user.add_randomness else 0),
		translation__language = request.LEARN_LANG,
	).extra(
		select = {'sum': 'score + priority'},
		order_by = ('sum', 'last_shown',)
	)[:amount]
	if not options:
		options = ActiveTranslation.objects.filter(
			learner = request.user,
			active = True,
			translation__language = request.LEARN_LANG,
		).extra(
			select = {'sum': 'score + priority'},
			order_by = ('sum', 'last_shown',)
		)[:amount]
		msg = 'There are not enough active phrases, so the minimum delay is ignored. You can control this in account settings.'
	if not options:
		options = ActiveTranslation.objects.filter(
			learner = request.user,
			translation__language = request.LEARN_LANG,
		).extra(
			select = {'sum': 'score + priority'},
			order_by = ('sum', 'last_shown',)
		)[:amount]
		msg = 'There are not enough active cards, so inactive phrases are shown and the minimum delay is ignored. You can activate lists for more phrases, control selection in account settings or change your learning language in the language menu.'
	if msg:
		add_message(request, WARNING, msg)
	return options


def weighted_option_choice(options):
	rnd = random() * sum(option.sum for option in options)
	for option in options:
		rnd -= option.sum
		if rnd < 0:
			return option