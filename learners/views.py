
from django.contrib.messages import add_message, INFO
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.utils.http import is_safe_url
from django.views.decorators.http import require_POST
from learners.forms import EmailLoginForm as LoginForm, LogoutForm, PasswordForm, ProfileForm
from learners.forms import RegistrationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import login_required
from settings import LOGIN_REDIRECT_URL
from basics.views import notification


def next_GET_or(url_name):
	"""
		Do you know decorators? Otherwise ignore.
	"""
	def next_GET(func):
		def func_with_next(request, *args, **kwargs):
			if url_name is None:
				next = LOGIN_REDIRECT_URL
			else:
				next = reverse(url_name)
			if 'next' in request.GET:
				if is_safe_url(url = request.GET['next'], host = request.get_host()):
					next = request.GET['next']
			return func(request, *args, next = next, **kwargs)
		return func_with_next
	return next_GET
next_GET = next_GET_or(None)


@next_GET
def login(request, next):
	if request.user.is_authenticated():
		return redirect(to = reverse('logout'))
	form = LoginForm(data = request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			auth_login(request, form.user)
			add_message(request, INFO, 'Welcome %s, you have been logged in!' % form.user)
			return redirect(to = request.POST['next'] or LOGIN_REDIRECT_URL)
	return render(request, 'login.html', {
		'form': form,
		'next': next,
	})


@require_POST
@next_GET
def logout(request, next):
	if not request.user.is_authenticated():
		return redirect(to = reverse('login'))
	form = LogoutForm(data = request.POST)
	if form.is_valid():
		auth_logout(request)
		add_message(request, INFO, 'You have been logged out. See you soon!')
		return redirect(to = request.POST['next'] or LOGIN_REDIRECT_URL)
	return notification(request, 'There was something wrong with the logout request. You have not been logged out.')


@login_required
@next_GET
def password(request, next):
	user = request.user
	form = PasswordForm(request.user, request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			user = authenticate(username = user.email, password = form.cleaned_data['new_password1'])
			auth_login(request, user)
			add_message(request, INFO, 'Your password has been changed.')
			return redirect(to = request.POST['next'] or LOGIN_REDIRECT_URL)
	return render(request, 'password.html', {
		'form': form,
		'next': next,
	})


@next_GET_or('profile')
def register(request, next):
	if request.user.is_authenticated():
		return redirect(to = reverse('logout'))
	form = RegistrationForm(request.POST or None, initial = {'next': next})
	if request.method == 'POST':
		if form.is_valid():
			user = form.save()
			user = authenticate(username = user.email, password = form.cleaned_data['password'])
			login(request, user)
			add_message(request, INFO, 'Your account %s has been created! Welcome to the site!' % user.email)
			return redirect(to = request.POST['next'] or LOGIN_REDIRECT_URL)
	return render(request, 'register.html', {
		'form': form,
	})


@login_required
@next_GET
def profile(request, next):
	form = ProfileForm(request.POST or None, instance = request.user)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			add_message(request, INFO, 'Your profile has been saved.')
			return redirect(to = reverse('profile'))
	return render(request, 'profile.html', {
		'profile_form': form,
		'logout_form': ProfileForm(None),
		'next': next,
	})


@login_required
def settings(request):
	return notification(request, 'There are no settings yet.')


