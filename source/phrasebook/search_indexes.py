
from haystack import indexes
from phrasebook.models import Translation


class TranslationIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document = True, use_template = True, template_name = 'translation.index')
	autocomplete = indexes.NgramField(model_attr = 'text')
	words = indexes.CharField(model_attr = 'text')
	romanization = indexes.CharField(model_attr = 'romanization')
	language = indexes.CharField(model_attr = 'language_disp')
	language_key = indexes.CharField(model_attr = 'language')
	other_languages = indexes.IntegerField(model_attr = 'other_languages')
	phrase_pk = indexes.IntegerField(model_attr = 'phrase_id')
	vote_score = indexes.IntegerField(model_attr = 'score')

	def get_model(self):
		return Translation

	#todo: filter out translations for phrases with public_view = False, if that option is not removed

