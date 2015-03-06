
from django.db import models
from django.utils.text import slugify
from learners.models import Learner
from phrasebook.models import Phrase


class PhraseList(models.Model):
	name = models.CharField(max_length = 48)
	phrases = models.ManyToManyField(Phrase, related_name = 'lists')
	public = models.BooleanField(default = False)

	def __unicode__(self):
		return self.name

	def slug(self):
		return slugify(self.name)


class ListAccess(models.Model):
	VIEW, EDIT = 'view', 'edit'
	phrase_list = models.ForeignKey(PhraseList)
	learner = models.ForeignKey(Learner)
	access = models.CharField(choices = ((VIEW, 'view list'), (EDIT, 'edit list')), max_length = 4)
	priority = models.SmallIntegerField(default = 0)
	active = models.BooleanField(default = False)

	class Meta:
		ordering = ('-priority',)

	def __unicode__(self):
		return '%s %s' % (self.learner, self.phrase_list)

#class ListEntry(models.Model):
#	phrase_list = models.ForeignKey(PhraseList, related_name = 'entries')
#	phrase = models.ForeignKey(Phrase, related_name = 'entries')


