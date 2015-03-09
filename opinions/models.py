
from django.db import models
from learners.models import Learner
from phrasebook.models import Translation


class TranslationUpVote(models.Model):
	translation = models.ForeignKey(Translation, related_name = 'upvotes')
	learner = models.ForeignKey(Learner)


class TranslationDownVote(models.Model):
	translation = models.ForeignKey(Translation, related_name = 'downvotes')
	learner = models.ForeignKey(Learner)


class TranslationComment(models.Model):
	translation = models.ForeignKey(Translation, related_name = 'comments')
	learner = models.ForeignKey(Learner)
	added = models.DateTimeField(auto_now_add = True)
	edited = models.DateTimeField(auto_now = True)
	text = models.TextField()


