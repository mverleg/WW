
"""
	Do you know Python decorators?
"""

from django.core.urlresolvers import reverse
from django.http import Http404
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


