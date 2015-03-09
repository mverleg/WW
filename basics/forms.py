
from django import forms
from settings import SUPPORTED_LANGUAGES


class ChooseLanguagesForm(forms.Form):
	"""
		The known language is called 'language' because it also sets the language of the website, which is called
		'language' in the standard code. This should not be a problem; the display name is given by 'label'.
	"""
	language = forms.ChoiceField(choices = SUPPORTED_LANGUAGES, required = True, label = 'Known language')
	learn = forms.ChoiceField(choices = SUPPORTED_LANGUAGES, required = True, label = 'Learning language')


