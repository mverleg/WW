
"""
	Models are the things that store data. The classes are the concepts, which automatically become tables in e.g. SQL.
	The instances are specific items, which become rows in the database.
"""

from django.db import models
from pinyin import get as to_pinyin
from learners.models import Learner
from settings import SUPPORTED_LANGUAGES


class Phrase(models.Model):
	"""
		This should be seen as a 'meaning'; there are different language 'implementations' of it.
	"""
	#todo you can add e.g. an image here, which would be the same for each language
	#todo: maybe public_view should not be optional, it would make things easier and more open
	learner = models.ForeignKey(Learner, blank = True, null = True, default = None)
	#public_view = models.BooleanField(default = True, verbose_name = 'publicly viewable')
	public_edit = models.BooleanField(default = True, verbose_name = 'publicly editable')

	def __unicode__(self):
		return 'phrase #%d' % self.pk

	#def clean(self, *args, **kwargs):
	#	if self.public_edit:
	#		self.public_view = True
	#	return super(Phrase, self).clean(*args, **kwargs)


class Translation(models.Model):
	"""
		This is a specific language version of the above Phrase (each phrase should have at least two languages to be useful).
	"""
	phrase = models.ForeignKey(Phrase, related_name = 'translations')
	language = models.CharField(choices = SUPPORTED_LANGUAGES, max_length = 8)
	text = models.TextField()

	def __unicode__(self):
		return self.text[:47] + '...' if len(self.text) > 50 else self.text

	def preview_text(self):
		return self.text[:47] + '...' if len(self.text) > 50 else self.text

	def other_languages(self):
		return Translation.objects.filter(phrase = self.phrase).count() - 1

	def phrase_pk(self):
		return self.phrase.pk

	def language_disp(self):
		return self.get_language_display().split('(')[0].strip()

	def get_votes(self):
		# this import needs to be here to prevent circular import problems
		from opinions.models import TranslationVote
		return TranslationVote.objects.filter(translation = self)

	@property
	def score(self):
		return sum([vote.score for vote in self.get_votes()], 0)

	def romanization(self):
		pin = to_pinyin(self.text)
		if not pin == self.text:
			return pin
		return ''


