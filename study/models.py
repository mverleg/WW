
from django.db import models
from learners.models import Learner
from phrasebook.models import Translation


class ActiveTranslation(models.Model):
	"""
		A user has a set of active phrases he is currently learning - he can limit the number of new ones.
		The phrases all have a score that is based on correct/incorrect answers (and possibly more); the lowest score card is asked next unless shown too recently.
	"""
	learner = models.ForeignKey(Learner)
	translation = models.ForeignKey(Translation)
	last_shown = models.PositiveIntegerField()
	""" Note that score is a derived property, stored for performance; it can be recalculated from other data. """
	score = models.FloatField()

	class Meta:
		unique_together = ('learner', 'translation',)


class Result(models.Model):
	CORRECT, INCORRECT, CLOSE = +1, -2, -1
	learner = models.ForeignKey(Learner)
	asked = models.ForeignKey(Translation, related_name = 'results_asked', help_text = 'The translation that was asked for (in presumably the target language)')
	known = models.ForeignKey(Translation, related_name = 'results_known', help_text = 'The translation that was shown (in presumably known language)')
	result = models.SmallIntegerField(choices = (
		(CORRECT, 'correct'),
		(INCORRECT, 'incorrect'),
		(CLOSE, 'not quite correct'),
	))
	when = models.DateTimeField(auto_now_add = True)

	class Meta:
		ordering = ('when',)


