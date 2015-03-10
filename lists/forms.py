
from django.forms import ModelForm
from lists.models import TranslationsList, ListAccess


class ListForm(ModelForm):
	class Meta:
		model = TranslationsList
		fields = ('name', 'public', 'language',)


class ListAccessForm(ModelForm):
	class Meta:
		model = ListAccess
		fields = ('priority', 'active',)