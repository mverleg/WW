
from django.forms import ModelForm, HiddenInput, TextInput
from phrasebook.models import Translation, Phrase


class EditPhraseForm(ModelForm):
	class Meta:
		model = Phrase
		fields = ('public_edit',)


class AddTranslationForm(ModelForm):
	class Meta:
		model = Translation
		fields = ('phrase', 'text', 'language',)
		widgets = {
			'phrase': HiddenInput(),
			'text': TextInput(),
		}


class PhraselessTranslationForm(ModelForm):
	class Meta:
		model = Translation
		fields = ('text', 'language',)
		widgets = {'text': TextInput(),}


