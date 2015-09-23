
from django.db import models
from learners.models import Learner
from phrasebook.models import Translation


class TranslationVote(models.Model):
	translation = models.ForeignKey(Translation, related_name = 'votes')
	up = models.BooleanField(default = True, help_text = 'Is this an upvote? (Otherwise it\'s a downvote)')
	learner = models.ForeignKey(Learner)
	""" This is a derived field for queries (saves quite some queries), don't set directly. """
	value = models.SmallIntegerField(help_text = 'Automatic field, don\'t edit! +1 for up, -1 for down')

	class Meta:
		unique_together = ('translation', 'learner',)

	def __str__(self):
		return '%s %svotes %s' % (self.learner, 'up' if self.up else 'down', self.translation)

	@property
	def score(self):
		return 1 if self.up else -1

	def save(self, *args, **kwargs):
		self.value = +1 if self.up else -1
		super(TranslationVote, self).save(*args, **kwargs)


class TranslationComment(models.Model):
	# (these are not visible/implemented yet)
	translation = models.ForeignKey(Translation, related_name = 'comments')
	learner = models.ForeignKey(Learner)
	added = models.DateTimeField(auto_now_add = True)
	edited = models.DateTimeField(auto_now = True)
	text = models.TextField()

	def __str__(self):
		return '%s comments on %s' % (self.learner, self.translation)

	def get_absolute_url(self):
		return self.translation.phrase.get_absolute_url()


