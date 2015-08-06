
from django import forms
from django.core.exceptions import ValidationError
from settings import SUPPORTED_LANGUAGES
from django.utils.translation import ugettext_lazy as _


class ChooseLanguagesForm(forms.Form):
	"""
		The known language is called 'language' because it also sets the language of the website, which is called
		'language' in the standard code. This should not be a problem; the display name is given by 'label'.
	"""
	language = forms.ChoiceField(choices = SUPPORTED_LANGUAGES, required = True, label = _(u'Known language'))
	learn = forms.ChoiceField(choices = SUPPORTED_LANGUAGES, required = True, label = _(u'Learning language'))

	def clean(self, *args, **kwargs):
		super(ChooseLanguagesForm, self).clean(*args, **kwargs)
		if self.cleaned_data['language'] == self.cleaned_data['learn']:
			raise ValidationError(_('You can\'t learn the same language you already know.'))
		return self.cleaned_data


