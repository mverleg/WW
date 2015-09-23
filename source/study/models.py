
from django.db import models
from learners.models import Learner
from phrasebook.models import Translation


class ActiveTranslation(models.Model):
	"""
		A user has a set of active phrases he is currently learning - he can limit the number of new ones.
		The phrases all have a score that is based on correct/incorrect answers (and possibly more); the lowest score phrase is asked next unless shown too recently.
	"""
	learner = models.ForeignKey(Learner)
	translation = models.ForeignKey(Translation)
	last_shown = models.PositiveIntegerField()
	""" Note that score, active and priority are derived properties, stored for performance; it can be recalculated from other data. """
	score = models.FloatField()
	priority = models.SmallIntegerField(default = 0)
	active = models.BooleanField(default = False)

	class Meta:
		unique_together = ('learner', 'translation',)
		ordering = ('score',)

	def __str__(self):
		return 'active "%s" for "%s"' % (self.translation, self.learner)


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
	verified = models.BooleanField(default = False, help_text = "True if the user typed the solution correctly, False otherwise (if he judged himself)")

	class Meta:
		ordering = ('-when',)

	def __str__(self):
		return '"%s" got "%s" %s' % (self.learner, self.asked, self.get_result_display())


