
"""
	Do you know Python decorators?
"""

from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render
from django.utils.http import is_safe_url
from settings import LOGIN_REDIRECT_URL


def instantiate(Model, in_kw_name = None, out_kw_name = None, model_attr_name = 'pk', model_attr_type = int):
	"""
		Turn an object key into an instance of that class.
	"""
	if out_kw_name is None:
		out_kw_name = Model.__name__.lower()
	if in_kw_name is None:
		in_kw_name = '%s_%s' % (out_kw_name, model_attr_name)
	def convert_to_instance_decorator(func):
		def func_with_instance(request, *args, **kwargs):
			identifier = kwargs.pop(in_kw_name)
			try:
				instance = Model.objects.get(**{model_attr_name: model_attr_type(identifier)})
			except Model.DoesNotExist:
				message = 'This page expects a %s with %s = %s, but no such %s was found.' % (Model.__name__, model_attr_name, identifier, Model.__name__)
				raise Http404(message)
			kwargs[out_kw_name] = instance
			return func(request, *args, **kwargs)
		return func_with_instance
	return convert_to_instance_decorator


def next_GET_or(url_name):
	"""
		Get the next page if it's provided through GET.
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


def confirm_first(message, subject = '', submit_text = 'continue', submit_class = 'btn-success', cancel_url_name = None):
	def actual_decorator(view_func):
		def wrapped_func(request, *args, **kwargs):
			''' check if this is a POST request and whether it's already confirmed '''
			if request.method == 'POST':
				if 'confirmed' not in request.POST:
					cancel_url = '/'
					if cancel_url_name:
						cancel_url = reverse(cancel_url_name)
					elif 'next' in request.POST:
						cancel_url = request.POST['next']
					return render(request, 'confirm_first.html', {
						'post': list(request.POST.items()),
						'subject': subject,
						'message': message,
						'cancel_url': cancel_url,
						'submit_url': '', # same page
						'submit_text': submit_text,
						'submit_class': submit_class,
					})
			''' not submitting or already confirmed '''
			return view_func(request, *args, **kwargs)
		return wrapped_func
	return actual_decorator

confirm_delete = confirm_first(message = 'Are you sure you want to delete this item?', subject = 'Delete?',
	submit_text = 'delete', submit_class = 'btn-danger')


