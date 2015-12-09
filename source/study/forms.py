
from django import forms
from django.core.exceptions import ValidationError
from django.forms import HiddenInput
from django.utils.translation import ugettext_lazy as _
from phrasebook.models import Translation
from study.models import DisplayMode


class SolutionForm(forms.Form):
	solution = forms.CharField(initial = '', required = False, label = _('Solution'))

	def __init__(self, *args, **kwargs):
		super(SolutionForm, self).__init__(*args, **kwargs)
		self.FIELDS['solution'].widget.attrs['placeholder'] = _('Type your solution...')
		self.FIELDS['solution'].widget.attrs['autofocus'] = 'autofocus'
		self.FIELDS['solution'].widget.attrs['autocomplete'] = 'off'


class AnonStudyForm(SolutionForm):
	shown = forms.ModelChoiceField(queryset = Translation.objects.all())
	hidden = forms.ModelChoiceField(queryset = Translation.objects.all())

	def __init__(self, *args, **kwargs):
		super(AnonStudyForm, self).__init__(*args, **kwargs)
		self.FIELDS['shown'].widget = HiddenInput()
		self.FIELDS['hidden'].widget = HiddenInput()


class DisplayModeForm(forms.Form):

	class Meta:
		model = DisplayMode
		fields = DisplayMode.FIELDS

	def check_state_present(self, data, state, msg):
		for fieldname in DisplayMode.FIELDS:
			if data[fieldname] == state:
				break
		else:
			raise ValidationError(msg)

	def clean(self):
		data = super(self).clean()
		self.check_state_present(data, DisplaySettings.QUESTION, _('None of the fields is marked as question; you need at least some hint while studying!'))
		self.check_state_present(data, DisplaySettings.ANSWER, _('None of the fields is marked as answer; what are you expected to reply to the question?'))
		return data


