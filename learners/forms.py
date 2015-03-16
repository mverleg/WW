
"""
	Form objects make the creation, checking and handling of HTML forms a lot easier. These specific ones can be
	ignored, but the concept will be useful.
"""

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordChangeForm


User = get_user_model()


class EmailLoginForm(forms.Form):

	email = forms.EmailField(max_length = 254)
	password = forms.CharField(widget = forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(EmailLoginForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs['placeholder'] = 'email@address.com'

	def clean(self):
		identifier = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		self.user = authenticate(username = identifier, password = password)
		if self.user is None:
			raise forms.ValidationError(
				message = 'there is no user with this email and password combination',
				code = 'invalid_login',
			)
		return self.cleaned_data


class LogoutForm(forms.Form):
	pass


PasswordForm = PasswordChangeForm


class ProfileForm(forms.ModelForm):
	class Meta:
		model = get_user_model()
		#todo: ask_direction should be a slider
		fields = ('name', 'ask_direction', 'add_randomness', 'minimum_delay', 'new_count', 'show_medium_correctness',
			'show_correct_count',)


class RegistrationForm(forms.ModelForm):
	"""
		registration form, inspired by http://stackoverflow.com/questions/16562529/django-1-5-usercreationform-custom-auth-model
	"""
	password = forms.CharField(label = 'Password', widget = forms.PasswordInput)
	password_confirm = forms.CharField(label = 'Password confirmation', widget = forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email',)

	def clean_password_confirm(self):
		password = self.cleaned_data.get('password')
		password_confirm = self.cleaned_data.get('password_confirm')
		if not password == password_confirm:
			raise forms.ValidationError('The passwords are not the same!')
		return password

	def save(self, commit = True):
		user = super(RegistrationForm, self).save(commit = False)
		password = self.cleaned_data.get('password')
		user.set_password(password)
		user.name = user.email.split('@')[0].replace('.', ' ').replace('-', ' ').replace('_', ' ').replace('  ', ' ').title()
		if commit:
			user.save()
		return user


