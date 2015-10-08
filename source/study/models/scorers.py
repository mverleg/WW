from django.db import models

from study.models.profile import StudyProfile


class Result(models.Model):
	"""
		Result of a single display of a flashcard (e.g. correct, incorrect, close).
	"""
	CORRECT, INCORRECT, CLOSE = +1, -2, -1
	scorer = models.ForeignKey(BaseScorer)
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
		return '"{0:s}" got "{1:s}" {2:s}'.format(self.learner, self.asked, self.get_result_display())


class BaseScorer(models.Model):
	"""
		Scorers keep track of the scores achieved for each card, as well as updating the score if an answer is given.
		As such, profiles that share a scorer share results. Note that this is independent of which cards are actually
		being asked, which is governed by Activator.
	"""
	name = models.CharField(max_length = 48)
	profile = models.ForeignKey(StudyProfile)

	def __str__(self):
		return '{0:s} [{1:s}]'.format(self.name, self.learner)


