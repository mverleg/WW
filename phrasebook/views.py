
from django.shortcuts import render
from basics.decorators import instantiate
from phrasebook.models import Phrase, Translation


@instantiate(Phrase, in_kw_name = 'pk', out_kw_name = 'phrase')
def show_phrase(request, phrase):
	#todo: there is of course room for improvement, e.g. show whether you have voted for an item, sort by number of votes and active language, ... These are not overly complicated but require some coding and queries (performance).
	translations = Translation.objects.filter(phrase = phrase)
	learn_translations, known_translations, other_translations = [], [], []
	for translation in translations:
		if translation.language == request.KNOWN_LANG:
			known_translations.append(translation)
		elif translation.language == request.LEARN_LANG:
			learn_translations.append(translation)
		else:
			other_translations.append(translation)
	return render(request, 'show_phrase.html', {
		'phrase': phrase,
		'translations': translations,
	})


