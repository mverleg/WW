
from django.shortcuts import render
from basics.views import notification


def study(request):
	return notification(request, 'No study yet!')


