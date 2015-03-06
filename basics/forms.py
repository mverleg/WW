
from django import forms
from settings import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE


class ChooseLanguageForm(forms.Form):

	language = forms.ChoiceField(choices = SUPPORTED_LANGUAGES, required = True)


