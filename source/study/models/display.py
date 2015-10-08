
from operator import itemgetter
from random import random
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class DisplayFixedSelector(models.Model):
	"""
		Every flashcard asks the same type of information (e.g. always 'ask image, answer written word in learning language')
	"""
	mode = models.ForeignKey(DisplayMode)

	def get_mode(self):
		return self.mode


class DisplayRandomSelector(models.Model):
	"""
		Pick a random display mode for each card based on relative weight.
	"""
	modes = models.ManyToManyField(DisplayMode, through = DisplayRandomNode)

	def get_mode(self):
		"""
			Weighted random sampling; in Python rather than database after all...
		"""
		nodes = list(DisplayRandomNode.objects.filter(selector = self).order_by('-weight'))
		random_weight = sum(node.weight for node in nodes) * random()
		weight = 0
		for node in nodes:
			weight += node.weight
			if weight > random_weight:
				return node
		raise AssertionError('shouldn\'t reach here')


class DisplayRandomNode(models.Model):
	mode = models.ForeignKey(DisplayMode)
	selector = models.ForeignKey(DisplayRandomSelector)
	weight = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(100)], default = 1)


class DisplayScoreProgressionSelector(models.Model):
	"""
		Pick a display mode based on the score of the current card.
	"""
	modes = models.ManyToManyField(DisplayMode, through = DisplayScoreProgressionNode)

	def get_mode(self):
		raise NotImplementedError('not made yet')  #todo (have a look at DisplayRandomSelector)


class DisplayScoreProgressionNode(models.Model):
	mode = models.ForeignKey(DisplayMode)
	selector = models.ForeignKey(DisplayScoreProgressionSelector)
	score = models.FloatField(default = 0)


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

	image = models.CharField(chocies = NOANSWER, max_length = 8, default = CONTEXT)
	writing_known = models.CharField(chocies = CHOICES, max_length = 8, default = QUESTION)
	phonetic_known = models.CharField(chocies = CHOICES, max_length = 8, default = HIDDEN)
	sound_known = models.CharField(chocies = NOANSWER, max_length = 8, default = QUESTION)
	writing_learning = models.CharField(chocies = CHOICES, max_length = 8, default = ANSWER)
	phonetic_learning = models.CharField(chocies = CHOICES, max_length = 8, default = HIDDEN)
	sound_learning = models.CharField(chocies = NOANSWER, max_length = 8, default = CONTEXT)
	examples = models.CharField(chocies = NOQUESTIONANSWER, max_length = 8, default = CONTEXT)

	FIELDS = ['image', 'writing_known', 'phonetic_known', 'sound_known', 'writing_learning', 'phonetic_learning', 'sound_learning', 'examples']


