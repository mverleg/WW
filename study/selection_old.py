
"""
	No longer used.
"""

from random import Random
from study.models import ActiveTranslation
from django.contrib.messages import WARNING, ERROR


def get_current_question(learner, known_language, learn_language):
	"""
		Get the current question and answer Translations. Uses a random seed but that's not needed anymore (but can't hurt, so I left it).

		This will not return a consistent result if
		* If the user changes language between question and answer.
		* If the user changes list settings between question and answer, then opens a page that reloads cache (study, stats).
		* If ANY user adds or removes phrases from a high-priority list.

		:return: hidden_translation, shown_translation, messages
	"""
	""" Use a fixed random seed, so that question and answer refer to the same translation. """
	lang_seed = sum(ord(letter) for letter in known_language) - sum(ord(letter) for letter in learn_language)
	randst = Random(x = learner.pk + learner.phrase_index + lang_seed)
	""" Get all ActiveTranslations to choose from. """
	msgs = []
	options = get_options(learner = learner, msgs = msgs, lang = learn_language, amount = 20)
	if not options:
		msgs.append((ERROR, 'You don\'t have enough phrases to start a quiz, sorry. You can add some active lists for more phrases!'))
		return
	""" Choose among the options. """
	learner.study_active = options[0]
	if learner.add_randomness:
		learner.study_active = weighted_option_choice(options, randst)
	""" Now get the other language versions. """
	other_li = learner.study_active.translation.phrase.translations.filter(language = known_language)
	#todo: order shown_li by votes to get the best one
	if not other_li:
		other_li = learner.study_active.translation.phrase.translations.exclude(language = learn_language)
	if not other_li:
		""" There is only one translation so we don't know what to ask. Disable the bad translation, try again (note that messages are intentionally lost). """
		msgs.append((ERROR, 'The phrase "%s" was skipped because there are no alternative language versions.' % learner.study_active.translation.text))
		learner.study_active.active = False
		learner.study_active.save()
		update_learner_actives(learner = learner)
		return get_current_question(learner, known_language, learn_language)
	""" Choice.translation is in the unknown language; should we show this or ask for this? """
	learner.save()
	if randst.random() * 100 < learner.ask_direction:
		""" We'll ask the learning language and show a (hopefully) known one. """
		hidden = learner.study_active.translation
		shown = other_li[0]
	else:
		hidden = other_li[0]
		shown = learner.study_active.translation
	return hidden, shown, msgs


def get_options(learner, msgs, lang, amount = 20):
	"""
		Returns ActiveTranslations sorted by urgency for the specified learner.
	"""
	msg = None
	options = ActiveTranslation.objects.filter(
		learner = learner,
		active = True,
		last_shown__lt = learner.phrase_index - learner.minimum_delay - (amount if learner.add_randomness else 0),
		translation__language = lang,
	).extra(
		#todo: score should also have a capped penalty for oldness (otherwise score never changes, so new phrases keep being added and old ones never show up again)
		select = {'sum': 'score + priority'},
		order_by = ('sum', 'last_shown',)
	)[:amount]
	if not options:
		options = ActiveTranslation.objects.filter(
			learner = learner,
			active = True,
			translation__language = lang,
		).extra(
			select = {'sum': 'score + priority'},
			order_by = ('sum', 'last_shown',)
		)[:amount]
		msg = 'There are not enough active phrases, so the minimum delay is ignored. You can control this in account settings.'
	if not options:
		options = ActiveTranslation.objects.filter(
			learner = learner,
			translation__language = lang,
		).extra(
			select = {'sum': 'score + priority'},
			order_by = ('sum', 'last_shown',)
		)[:amount]
		msg = 'There are not enough active translations, so inactive phrases are shown and the minimum delay is ignored. You can activate lists for more phrases, control selection in account settings or change your learning language in the language menu.'
	if msg:
		msgs.append((WARNING, msg))
	return options


def weighted_option_choice(options, random_state):
	"""
		From a list of items with a 'sum' attribute, choose a random one with an unnormalized probability of::

			1 / max(sum, 1)
	"""
	for option in options:
		option._prob = 1 / max(option.sum, 1)
	tot = sum(option._prob for option in options)
	if tot <= 0:
		return random_state.choice(options)
	rnd = random_state.random() * tot
	for option in options:
		rnd -= option._prob
		if rnd < 0:
			return option


