
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from basics.views import notification


@login_required
@require_POST
def add_translation_vote(request):
	pass


@login_required
@require_POST
def delete_translation_vote(request):
	pass


@login_required
def add_translation_comment(request):
	return notification(request, 'Not implemented')


@login_required
def delete_translation_comment(request):
	return notification(request, 'Not implemented')


