from django.core.urlresolvers import reverse
from django.db import models
from learners.models import Learner
from phrasebook.models import Translation


class TranslationVote(models.Model):
	translation = models.ForeignKey(Translation, related_name = 'upvotes')
	up = models.BooleanField(default = True, help_text = 'Is this an upvote? (Otherwise it\'s a downvote)')
	learner = models.ForeignKey(Learner)

	class Meta:
		unique_together = ('translation', 'learner',)

	def __unicode__(self):
		return u'%s %svotes %s' % (self.learner, 'up' if self.up else 'down', self.translation)

	@property
	def score(self):
		return 1 if self.up else -1


class TranslationComment(models.Model):
	# (these are not ivisible/implemented yet)
	translation = models.ForeignKey(Translation, related_name = 'comments')
	learner = models.ForeignKey(Learner)
	added = models.DateTimeField(auto_now_add = True)
	edited = models.DateTimeField(auto_now = True)
	text = models.TextField()

	def __unicode__(self):
		return u'%s comments on %s' % (self.learner, self.translation)

	def get_absolute_url(self):
		return self.translation.phrase.get_absolute_url()


