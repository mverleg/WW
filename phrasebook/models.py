
"""
	Models are the things that store data. The classes are the concepts, which automatically become tables in e.g. SQL.
	The instances are specific items, which become rows in the database.
"""

from django.db import models
from settings import SUPPORTED_LANGUAGES


class Phrase(models.Model):
	"""
		This should be seen as a 'meaning'; there are different language 'implementations' of it.
	"""
	#todo you can add e.g. an image here, which would be the same for each language
	#todo you could also have categories and comments

	def __unicode__(self):
		return 'phrase #%d' % self.pk


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


