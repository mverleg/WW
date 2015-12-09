
from operator import itemgetter
from random import random
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from model_utils.managers import InheritanceManager


class DisplayMode(models.Model):
	"""
		A class that controls what is displayed for a flashcard.
	"""
	QUESTION, ANSWER, CONTEXT, HIDDEN = 'question', 'answer', 'context', 'hidden'
	CHOICES = (
		(QUESTION, 'Question: show in the question to be answered.'),
		(ANSWER, 'Answer: what the learner should provide as answer.'),
		(CONTEXT, 'Context: reveal as extra info afterwards.'),
		(HIDDEN, 'Hidden: ignore this information.'),
	)
	NOANSWER = itemgetter(0, 2, 3)(CHOICES)
	NOQUESTIONANSWER = itemgetter(2, 3)(CHOICES)

	image = models.CharField(choices = NOANSWER, max_length = 8, default = CONTEXT)
	writing_known = models.CharField(choices = CHOICES, max_length = 8, default = QUESTION)
	phonetic_known = models.CharField(choices = CHOICES, max_length = 8, default = HIDDEN)
	sound_known = models.CharField(choices = NOANSWER, max_length = 8, default = QUESTION)
	writing_learning = models.CharField(choices = CHOICES, max_length = 8, default = ANSWER)
	phonetic_learning = models.CharField(choices = CHOICES, max_length = 8, default = HIDDEN)
	sound_learning = models.CharField(choices = NOANSWER, max_length = 8, default = CONTEXT)
	examples = models.CharField(choices = NOQUESTIONANSWER, max_length = 8, default = CONTEXT)

	FIELDS = ['image', 'writing_known', 'phonetic_known', 'sound_known', 'writing_learning', 'phonetic_learning', 'sound_learning', 'examples']

	def __str__(self):
		# unused?
		return '-'.join((
			'image', self.image,
			'writing_known', self.writing_known,
			'phonetic_known', self.phonetic_known,
			'sound_known', self.sound_known,
			'writing_learning', self.writing_learning,
			'phonetic_learning', self.phonetic_learning,
			'sound_learning', self.sound_learning,
			'examples', self.examples,
		))

	def hash(self):
		# unused
		mp = {'question': 2, 'answer': 1, 'context': 0, 'hidden': 0}
		vals = [self.image, self.writing_known, self.phonetic_known, self.sound_known, self.writing_learning, self.phonetic_learning, self.sound_learning, self.examples]
		print(vals)
		print([(3**k)*mp[val] for k, val in enumerate(vals)])
		return sum((3**k)*mp[val] for k, val in enumerate(vals))


class BaseDisplaySelector(models.Model):
	"""
		Base display selector that the others extend (non-abstract for ForeignKeys).
	"""
	info = '(no info o n base selector)'  # todo: not used atm
	name = models.CharField(max_length = 48)
	profile = models.ForeignKey('study.StudyProfile')

	objects = InheritanceManager()


class DisplayFixedSelector(BaseDisplaySelector):
	"""
		Every flashcard asks the same type of information (e.g. always 'ask image, answer written word in learning language')
	"""
	info = 'Simple: always ask the same thing (e.g. always show the image and request the written name).'
	mode = models.ForeignKey(DisplayMode)

	def get_mode(self):
		return self.mode


class DisplayRandomMode(DisplayMode):
	# mode = models.ForeignKey(DisplayMode)
	# selector = models.ForeignKey(DisplayRandomSelector)
	weight = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(100)], default = 1)


class DisplayRandomSelector(BaseDisplaySelector):
	"""
		Pick a random display mode for each card based on relative weight.
	"""
	info = 'Random: weighted-randomly select what to show and ask.'
	modes = models.ManyToManyField(DisplayRandomMode)

	def get_mode(self):
		"""
			Weighted random sampling; in Python rather than database after all...
		"""
		nodes = list(DisplayRandomMode.objects.filter(selector = self).order_by('-weight'))
		random_weight = sum(node.weight for node in nodes) * random()
		weight = 0
		for node in nodes:
			weight += node.weight
			if weight > random_weight:
				return node
		raise AssertionError('shouldn\'t reach here')


class DisplayScoreProgressionMode(models.Model):
	mode = models.ForeignKey(DisplayMode)
	selector = models.ForeignKey('study.DisplayScoreProgressionSelector')
	score = models.FloatField(default = 0)


class DisplayScoreProgressionSelector(BaseDisplaySelector):
	"""
		Pick a display mode based on the score of the current card.
	"""
	info = 'Score: change the questions based on score (e.g. pronunciation first, writing after).'
	modes = models.ManyToManyField(DisplayMode, through=DisplayScoreProgressionMode)

	def get_mode(self):
		raise NotImplementedError('not made yet')  #todo (have a look at DisplayRandomSelector)


