
from random import sample, random
from math import exp
from django.db.models import Sum
from study.models import ActiveTranslation
from django.contrib.messages import WARNING


def get_next_question(learner, known_language, learn_language):
	"""
		Randomly get a question to ask the user, showing low scoring cards more.

		:return: active_transation, hidden_translation, shown_translation, messages
	"""
	msgs = []
	""" Get all options """
	actives = get_all_options(learner = learner, msgs = msgs, learn_language = learn_language, limit = 100)
	""" Choose a random option to show """
	for active in actives:
		active._energy = active.score + active.priority
	while actives:
		chosen_active = weighted_sample(options = actives, scale = 1e-3 * learner.favor_unknown)
		"""
			Find matching other language pairs (active > translation > phrase > translations = siblings)
		"""
		known_translations = list(chosen_active.translation.phrase.translations.filter(language = known_language) \
			.annotate(vote_value = Sum('votes__value')).order_by('-vote_value'))
		""" Next line is because 'no votes' gives None in the query, which ranks below negative numbers in sorting. """
		known_translations.sort(key = lambda kt: 0 if kt.vote_value is None else kt.vote_value)
		print([kt.vote_value for kt in known_translations])  # todo: test after phrase activation works properly
		try:
			known_translation = known_translations[0]
		except IndexError:
			actives.remove(chosen_active)
			continue
		""" Choose which one is shown and which hidden """
		if random() * 100 < learner.ask_direction:
			""" We'll ask the learning language and show a (hopefully) known one. """
			return chosen_active, chosen_active.translation, known_translation, msgs
		else:
			return chosen_active, known_translation, chosen_active.translation, msgs
	raise ActiveTranslation.DoesNotExist('There is no translation that matches the criteria.')


def get_all_options(learner, msgs, learn_language, limit = None):
	"""
		Get all the ActiveTranslation options for this user and language, ignoring first minimum_delay and then active
		state if there aren't enough results otherwise. If there are too many results, some are selected at random.
		(I know what you're thinking: don't get all of them out of the database then! Well, random selection from the
		database is really, really slow, and I can't know the PKs without getting them all so I can't use __in)
	"""
	msg = None
	print(learner.phrase_index, learner.minimum_delay)
	actives = list(ActiveTranslation.objects.filter(
		learner = learner,
		translation__language = learn_language,
		last_shown__lt = learner.phrase_index - learner.minimum_delay,
		active = True,
	).order_by('priority'))
	if not actives:
		actives = list(ActiveTranslation.objects.filter(
			learner = learner,
			translation__language = learn_language,
			active = True,
		).order_by('priority'))
		msg = 'There are not enough active phrases, so the minimum delay is ignored. You can add more active phrases by expanding your lists, or control delay in account settings.'
	if not actives:
		actives = list(ActiveTranslation.objects.filter(
			learner = learner,
			translation__language = learn_language,
		).order_by('priority'))
		msg = 'There are not enough active phrases, so the minimum delay is ignored and inactive phrases are shown. You can add more active phrases by expanding your lists, or control the delay in account settings.'
	if msg:
		msgs.append((WARNING, msg,))
	if limit:
		if len(actives) > limit:
			return sample(actives, 100)
	return actives


def weighted_sample(options, scale = 1.):
	"""
		For a list of items with an '_energy' property, sample from them using exp(-E*scale) unnormalized probabilities.
		It's fastest if the values are sorted by ascending _energy.
	"""
	""" Calculate the relative probability of each option. """
	total = 0.
	for option in options:
		option._partition = exp(- option._energy * scale)
		total += option._partition
	""" Sample using the calculated _partition values. """
	rnd = random() * total
	for option in options:
		rnd -= option._partition
		if rnd < 0:
			return option


