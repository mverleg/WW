
from random import Random
from django.db.transaction import atomic
from lists.models import ListAccess
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
	""" Use a fixed random seed, so that question and answer refer to the same card. """
	lang_seed = sum(ord(letter) for letter in known_language) - sum(ord(letter) for letter in learn_language)
	randst = Random(x = learner.pk + learner.phrase_index + lang_seed)
	""" Get all ActiveTranslations to choose from. """
	msgs = []
	options = get_options(learner = learner, msgs = msgs, lang = learn_language)
	if not options:
		msgs.append((ERROR, 'You don\'t have enough phrases to start a quiz, sorry. You can add some active lists for more phrases!'))
		return
	""" Choose among the options. """
	choice = options[0]
	if learner.add_randomness:
		choice = weighted_option_choice(options, randst)
	""" Now get the other language versions. """
	other_li = choice.translation.phrase.translations.filter(language = known_language)
	#todo: order shown_li by votes to get the best one
	if not other_li:
		other_li = choice.translation.phrase.translations.exclude(language = learn_language)
	if not other_li:
		""" There is only one translation so we don't know what to ask. Disable the bad card, try again (note that messages are intentionally lost). """
		msgs.append((ERROR, 'The phrase "%s" was skipped because there are no alternative language versions.' % choice.translation.text))
		choice.active = False
		choice.save()
		update_learner_actives(learner = learner)
		return get_current_question(learner, known_language, learn_language)
	""" Choice.translation is in the unknown language; should we show this or ask for this? """
	if randst.random() * 100 < learner.ask_direction:
		""" We'll ask the learning language and show a (hopefully) known one. """
		hidden = choice.translation
		shown = other_li[0]
	else:
		hidden = other_li[0]
		shown = choice.translation
	return hidden, shown, msgs


@atomic
def update_learner_actives(learner, specific_translation = None, force = False):
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
	for active in actives_map.values():
		active.save()
	learner.need_active_update = False
	learner.save()


def get_options(learner, msgs, lang, amount=20):
	"""
		Returns amount ActiveTranslations for the specified learner.
	"""
	msg = None
	options = ActiveTranslation.objects.filter(
		learner = learner,
		active = True,
		last_shown__lt = learner.phrase_index - learner.minimum_delay - (amount if learner.add_randomness else 0),
		translation__language = lang,
	).extra(
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
		msg = 'There are not enough active cards, so inactive phrases are shown and the minimum delay is ignored. You can activate lists for more phrases, control selection in account settings or change your learning language in the language menu.'
	if msg:
		msgs.append((WARNING, msg))
	return options


def add_more_active_phrases(learner, msgs):
	# how many active now
	unlearned_count = ActiveTranslation.objects.filter(active = True, score__lte = 0).count()
	# how many active max
	goal_count = learner.new_count
	# add more according to priority until satisfied
	if unlearned_count < goal_count:
		# get possible translations to add (options)
		accesses = ListAccess.objects.filter(learner = learner, active = True).order_by('-priority')
		options = sum([list(access.translations_list.translations.all()) for access in accesses], [])
		already_active_pks = [active.translation.pk for active in ActiveTranslation.objects.filter(learner = learner)]
		# add them one by one (order of decreasing priority) until enough
		cnt = goal_count - unlearned_count
		for option in options:
			if option.pk not in already_active_pks:
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
	msgs.append((WARNING, 'Tried to add more cards to the active collection but it seems there are not enough left in your lists.'))
	#todo: maybe use some random sampling when choosing which phrase to activate


def weighted_option_choice(options, random_state):
	tot = sum(option.sum for option in options)
	if tot <= 0:
		return random_state.choice(options)
	rnd = random_state.random() * tot
	for option in options:
		rnd -= option.sum
		if rnd < 0:
			return option


