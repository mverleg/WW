
from django.core.exceptions import ValidationError
from django import forms


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


