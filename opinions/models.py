
from django.db import models
from learners.models import Learner
from phrasebook.models import Translation


class TranslationVote(models.Model):
	translation = models.ForeignKey(Translation, related_name = 'upvotes')
	up = models.BooleanField(default = True, help_text = 'Is this an upvote? (Otherwise it\'s a downvote)')
	learner = models.ForeignKey(Learner)

	def __unicode__(self):
		return '%s %svotes %s' % (self.learner, 'up' if self.up else 'down', self.translation)


class TranslationComment(models.Model):
	translation = models.ForeignKey(Translation, related_name = 'comments')
	learner = models.ForeignKey(Learner)
	added = models.DateTimeField(auto_now_add = True)
	edited = models.DateTimeField(auto_now = True)
	text = models.TextField()

	def __unicode__(self):
		return '%s comments on %s' % (self.learner, self.translation)


