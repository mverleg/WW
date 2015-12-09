
from django.conf import settings
from django.db.transaction import atomic
from django.utils.translation import ugettext_lazy as _
from lists.models import ListAccess
from study.models import ActiveTranslation, DisplayRandomMode, DisplayMode, DisplayRandomSelector, \
	PriorityLimitedActivator, LinearScorer, SimplePhraseChooser, StudyProfile
from django.contrib.messages import WARNING


@atomic
def update_learner_actives(learner, specific_translation = None, force = False):
	"""
		If needed (or force is True), update all the learner's ActiveTranslation .priority and .active properties.
	"""
	#todo: note that actives need updating when a list changes or a card is activated or on reset, priority only when a list changes or on reset and score only on reset
	#todo: is this active about "in an active list" or about "activated for showing"? [first one]
	if not (force or learner.need_active_update):
		return
	accesses = ListAccess.objects.filter(learner = learner, active = True)
	actives_map = {active.translation.pk: active for active in ActiveTranslation.objects.filter(learner = learner)}
	for pk, active in list(actives_map.items()):
		active.active = False
		active.priority = 0
	for access in accesses:
		if specific_translation:
			translations = [specific_translation]
		else:
			translations = access.translations_list.translations.all()
		for translation in translations:
			if not translation.pk in actives_map:
				continue
			active = actives_map[translation.pk]
			active.active = True
			if access.priority > active.priority:
				active.priority = access.priority
	for active in list(actives_map.values()):
		active.save()
	learner.need_active_update = False
	learner.save()


def add_more_active_phrases(learner, msgs, lang):
	print('adding more active phrases')  #todo: remove print
	""" how many active now """
	unlearned_count = ActiveTranslation.objects.filter(active = True, score__lte = 0, translation__language = lang).count()
	""" how many active max """
	goal_count = learner.new_count
	""" add more according to priority until satisfied """
	if unlearned_count < goal_count:
		""" get possible translations to add (options) """
		accesses = ListAccess.objects.filter(learner = learner, active = True).order_by('-priority')
		options = sum([list(access.translations_list.translations.all()) for access in accesses], [])
		already_active_pks = [active.translation.pk for active in ActiveTranslation.objects.filter(learner = learner)]
		""" add them one by one (order of decreasing priority) until enough """
		cnt = goal_count - unlearned_count
		for option in options:
			if option.pk not in already_active_pks and option.language == lang:
				ActiveTranslation(
					learner = learner,
					translation = option,
					last_shown = 0,
					score = 0,
				).save()
				cnt -= 1
				if cnt <= 0:
					learner.need_update()
					return
	msgs.append((WARNING, 'Tried to add more phrases to the active collection but it seems there are not enough left in your lists for the current language.'))
	#todo: maybe use some random sampling when choosing which phrase to activate


def make_default_profile(learner=None, learn_language=settings.DEFAULT_LEARN_LANGUAGE, known_language=None):
	"""
	Create a simple profile including all derived fields. E.g. for when making a new user account.
	"""
	modeL = DisplayRandomMode(
		writing_known=DisplayMode.QUESTION,
		sound_known=DisplayMode.QUESTION,
		writing_learning=DisplayMode.ANSWER,
		sound_learning=DisplayMode.CONTEXT,
		image=DisplayMode.CONTEXT,
		examples=DisplayMode.CONTEXT,
		weight=60,
	)
	modeK = DisplayRandomMode(
		writing_known=DisplayMode.ANSWER,
		sound_known=DisplayMode.CONTEXT,
		writing_learning=DisplayMode.QUESTION,
		sound_learning=DisplayMode.QUESTION,
		image=DisplayMode.CONTEXT,
		examples=DisplayMode.CONTEXT,
		weight=40,
	)
	modeL.save()
	modeK.save()
	display_selector = DisplayRandomSelector()
	display_selector.save()
	display_selector.add(modeL)
	display_selector.add(modeK)

	activator = PriorityLimitedActivator()
	activator.save()

	scorer = LinearScorer()
	scorer.save()

	phrase_chooser = SimplePhraseChooser()
	phrase_chooser.save()

	profile = StudyProfile(
		name=_('default'),
		learner=learner,
		learn_language=learn_language,
		known_language=known_language,
		display_selector=display_selector,
		activator=activator,
		scorer=scorer,
		phrase_chooser=phrase_chooser
	)

	profile.save()
	return profile