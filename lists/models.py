
from django.db import models
from django.utils.text import slugify
from learners.models import Learner
from phrasebook.models import Phrase


class TranslationsList(models.Model):
	name = models.CharField(max_length = 48, help_text = 'What is this list called? E.g. "Chinese animal names"')
	phrases = models.ManyToManyField(Phrase, related_name = 'lists')
	public = models.BooleanField(default = True, help_text = 'Can anyone follow this list?')

	def __unicode__(self):
		return self.name

	def slug(self):
		return slugify(self.name)


class ListAccess(models.Model):
	VIEW, EDIT = 'view', 'edit'
	translation_list = models.ForeignKey(TranslationsList)
	learner = models.ForeignKey(Learner)
	access = models.CharField(choices = ((VIEW, 'view list'), (EDIT, 'edit list')), max_length = 4)
	priority = models.SmallIntegerField(default = 0)
	active = models.BooleanField(default = False)

	class Meta:
		ordering = ('-priority',)

	def __unicode__(self):
		return '%s %s' % (self.learner, self.phrase_list)


