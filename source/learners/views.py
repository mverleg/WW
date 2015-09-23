
from django.contrib.messages import add_message, INFO
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from basics.decorators import next_GET, next_GET_or
from learners.forms import EmailLoginForm as LoginForm, LogoutForm, PasswordForm, ProfileForm
from learners.forms import RegistrationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import login_required
from settings import LOGIN_REDIRECT_URL
from basics.views import notification
from study.functions import update_learner_actives, add_more_active_phrases


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


@next_GET
def logout(request, next):
	if not request.method == 'POST':
		return redirect(to = reverse('home'))
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
			auth_login(request, user)
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
			return redirect(to = request.POST['next'] or reverse('profile'))
	return render(request, 'profile.html', {
		'profile_form': form,
		'logout_form': ProfileForm(None),
		'next': next,
	})


@require_POST
@login_required
def reset(request):
	"""
		Reset some stuff for the user, just in case anything goes wrong.
	"""
	request.user.study_shown = None
	request.user.study_hidden = None
	request.user.study_state = request.user.NOTHING
	request.user.study_answer = ''
	#todo: reset some settings (and warn about that in template)
	request.user.save()
	update_learner_actives(learner = request.user, force = True)
	add_more_active_phrases(learner = request.user, lang = request.LEARN_LANG, msgs = [])
	update_learner_actives(learner = request.user)
	add_message(request, INFO, 'Cache properties reset for "%s"' % request.user.email)
	request.session.clear()
	return redirect(reverse('profile'))


#@login_required
#def settings(request):
#	return notification(request, 'There are no settings yet.')


