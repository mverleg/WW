
from django.forms import ModelForm
from lists.models import TranslationsList


class ListForm(ModelForm):
	class Meta:
		model = TranslationsList
		fields = ('name', 'public',)


