
from django import forms
from django.forms import HiddenInput
from django.utils.translation import ugettext_lazy as _
from phrasebook.models import Translation


class SolutionForm(forms.Form):
	solution = forms.CharField(initial = '', required = False, label = _('Solution'))

	def __init__(self, *args, **kwargs):
		super(SolutionForm, self).__init__(*args, **kwargs)
		self.fields['solution'].widget.attrs['placeholder'] = _('Type your solution...')
		self.fields['solution'].widget.attrs['autofocus'] = 'autofocus'


class AnonStudyForm(SolutionForm):
	shown = forms.ModelChoiceField(queryset = Translation.objects.all())
	hidden = forms.ModelChoiceField(queryset = Translation.objects.all())

	def __init__(self, *args, **kwargs):
		super(AnonStudyForm, self).__init__(*args, **kwargs)
		self.fields['shown'].widget = HiddenInput()
		self.fields['hidden'].widget = HiddenInput()


