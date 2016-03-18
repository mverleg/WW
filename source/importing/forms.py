
from django.conf import settings
from django.core.exceptions import ValidationError
from django import forms
from re import findall, split
from lists.models import TranslationsList, ListAccess
from phrasebook.models import Translation, Phrase


class ImportForm(forms.Form):
	text = forms.CharField(required = False, widget = forms.Textarea(attrs = {'rows': 20, 'cols': 100}))
	file = forms.FileField(required = False)

	def __init__(self, data, files, *args, **kwargs):
		super(ImportForm, self).__init__(data, files, *args, **kwargs)
		self.file_content = None
		if files:
			if 'file' in files:
				self.file_content = files['file'].read().decode('utf-8')

	def clean(self):
		if not (self.cleaned_data.get('text', '').strip() or self.cleaned_data.get('file', None)):
			raise ValidationError('Either enter a text or upload a file.')

	def get_content(self):
		if not self.is_valid():
			raise Exception('This only works on validated forms.')
		if self.cleaned_data['text'].strip():
			return self.cleaned_data['text']
		return self.file_content


class ChinesepodForm(forms.Form):
	COOKIE_NAME = 'CPODSESSID'
	urls = forms.CharField(widget = forms.Textarea, help_text = 'You can paste a url like "https://chinesepod.com/lessons/haggle-for-a-good-deal", or multiple separated by newlines.')
	session = forms.CharField(widget = forms.PasswordInput, help_text = 'Copy the value of "{0:s}" cookie (or in cookie header format).'.format(COOKIE_NAME))
	#todo: write instructions how to get cookie value

	def clean_session(self):
		session = self.cleaned_data['session']
		if '=' in session:
			if not self.COOKIE_NAME in session:
				raise ValidationError('Using cookie header format but "{0:s}" was not found.'.format(self.COOKIE_NAME))
			try:
				session = findall(r'{0:s}=([A-Za-z0-9]+)(?:;|$)'.format(self.COOKIE_NAME), session)[0]
			except IndexError: pass
		if not session.isalnum():
			raise ValidationError('Session did not have the expected format (no cookie header format found but does contain non-alphanumeric characters).')
		return session


class TextForm(forms.Form):
	text = forms.CharField(required=True, widget = forms.Textarea(attrs=dict(rows=20, cols=100)))
	list = forms.ModelChoiceField(TranslationsList)
	public_edit = forms.BooleanField(initial=True, label='Publicly editable')

	def __init__(self, learner, *args, **kwargs):
		super(TextForm, self).__init__(*args, **kwargs)
		self.fields['list'].queryset = TranslationsList.objects.filter(followers__in=
			ListAccess.objects.filter(learner=learner, access=ListAccess.EDIT))


