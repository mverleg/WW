from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from learners.models import Learner
from phrasebook.models import Phrase, Translation
from settings import SUPPORTED_LANGUAGES


class TranslationsList(models.Model):
	name = models.CharField(max_length = 48, help_text = 'What is this list called? E.g. "Chinese animal names"')
	translations = models.ManyToManyField(Translation, related_name = 'lists', blank = True)
	public = models.BooleanField(default = True, help_text = 'Can anyone follow this list?')
	language = models.CharField(choices = SUPPORTED_LANGUAGES, max_length = 8, blank = True, null = True, help_text = 'You can select the language to learn for this list, or leave it blank for a mixed-language list.')

	class Meta:
		verbose_name = 'list'

	def __unicode__(self):
		return self.name

	@property
	def slug(self):
		return slugify(self.name)

	def language_disp(self):
		return self.get_language_display().split('(')[0].strip()

	def get_absolute_url(self):
		return reverse('show_list', kwargs = {'pk': self.pk, 'slug': self.slug})


class ListAccess(models.Model):
	VIEW, EDIT = 'view', 'edit'
	translations_list = models.ForeignKey(TranslationsList)
	learner = models.ForeignKey(Learner)
	access = models.CharField(choices = ((VIEW, 'view list'), (EDIT, 'edit list')), max_length = 4)
	priority = models.SmallIntegerField(default = 0, help_text = 'Higher priority lists will show up more during learning sessions (only applies to you).')
	active = models.BooleanField(default = False, help_text = 'Inactive lists don\'t show up during learning sessions (only applies to you).')

	class Meta:
		ordering = ('-priority',)

	def __unicode__(self):
		return u'%s %s' % (self.learner, self.translations_list)

	@property
	def editable(self):
		return self.access == ListAccess.EDIT


