# -*- coding: utf-8 -*-

"""
	Models are the things that store data. The classes are the concepts, which automatically become tables in e.g. SQL.
	The instances are specific items, which become rows in the database.
"""

from django.core.urlresolvers import reverse
from django.db import models
from pinyin import get as to_pinyin
from basics.functions import get_in_each_language
from learners.models import Learner
from settings import SUPPORTED_LANGUAGES


class Phrase(models.Model):
	"""
		This should be seen as a 'meaning'; there are different language 'implementations' of it.
	"""
	#todo you can add e.g. an image here, which would be the same for each language
	#todo: maybe public_view should not be optional, it would make things easier and more open
	learner = models.ForeignKey(Learner, blank = True, null = True, default = None)
	public_edit = models.BooleanField(default = True, verbose_name = 'publicly editable')

	def __str__(self):
		return 'phrase #%d' % self.pk

	def get_absolute_url(self):
		return reverse('show_phrase', kwargs = {'pk': self.pk})

	def public_lists(self):
		from lists.models import TranslationsList
		lists = []
		for translation in Translation.objects.filter(phrase = self):
			for li in TranslationsList.objects.filter(translations = translation, public = True):
				if li not in lists:
					lists.append(li)
		return lists


class Translation(models.Model):
	"""
		This is a specific language version of the above Phrase (each phrase should have at least two languages to be useful).
	"""
	phrase = models.ForeignKey(Phrase, related_name = 'translations')
	language = models.CharField(choices = SUPPORTED_LANGUAGES, max_length = 8)
	text = models.TextField()

	def __str__(self):
		return self.text[:47] + '...' if len(self.text) > 50 else self.text

	def preview_text(self):
		return self.text[:47] + '...' if len(self.text) > 50 else self.text

	def other_languages(self):
		return Translation.objects.filter(phrase = self.phrase).count() - 1

	def phrase_pk(self):
		return self.phrase.pk

	def language_disp(self):
		return self.get_language_display().split('(')[0].strip()

	def language_all(self):
		""" This makes sure you can search for 荷兰语 and get all English phrases """
		return ' '.join(get_in_each_language(self.get_language_display()))

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

	def get_absolute_url(self):
		return self.phrase.get_absolute_url()


