
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError
from django.forms import HiddenInput
from settings import SUPPORTED_LANGUAGES
from django.utils.translation import ugettext_lazy as _


class ChooseLanguagesForm(forms.Form):
	"""
		The known language is called 'language' because it also sets the language of the website, which is called
		'language' in the standard code. This should not be a problem; the display name is given by 'label'.
	"""
	language = forms.ChoiceField(choices = SUPPORTED_LANGUAGES, required = True, label = _('Known language'))
	learn = forms.ChoiceField(choices = SUPPORTED_LANGUAGES, required = True, label = _('Learning language'))
	next = forms.CharField(widget=HiddenInput)

	def clean(self, *args, **kwargs):
		super(ChooseLanguagesForm, self).clean(*args, **kwargs)
		if self.cleaned_data['language'] == self.cleaned_data['learn']:
			raise ValidationError(_('You can\'t learn the same language you already know.'))
		return self.cleaned_data

	@property
	def helper(self):
		helper = FormHelper(self)
		helper.form_action = 'choose_languages'
		helper.add_input(Submit('', 'Change', css_class = 'pull-right'))
		return helper


