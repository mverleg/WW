
from django import forms
from django.utils.translation import ugettext_lazy as _


class SolutionForm(forms.Form):
	solution = forms.CharField(initial = '', required = False, label = _('Solution'))

	def __init__(self, *args, **kwargs):
		super(SolutionForm, self).__init__(*args, **kwargs)
		self.fields['solution'].widget.attrs['placeholder'] = _('Type your solution...')


