
"""
	This is from https://github.com/pinax/django-forms-bootstrap#django-forms-bootstrap
"""

from django import template
from django.template import Context
from django.template.loader import get_template


register = template.Library()


def _preprocess_fields(form):
	"""
		This is from https://github.com/pinax/django-forms-bootstrap#django-forms-bootstrap
	"""
	for field in form.fields:
		name = form.fields[field].widget.__class__.__name__.lower()
		if not name.startswith("radio") and not name.startswith("checkbox"):
			try:
				form.fields[field].widget.attrs["class"] += " form-control"
			except KeyError:
				form.fields[field].widget.attrs["class"] = " form-control"
	return form


@register.filter
def as_bootstrap(form):
	"""
		This is from https://github.com/pinax/django-forms-bootstrap#django-forms-bootstrap
	"""
	template = get_template("bootstrap/form.html")
	form = _preprocess_fields(form)

	c = Context({
		"form": form,
	})
	return template.render(c)


@register.filter
def css_class(field):
	"""
		This is from https://github.com/pinax/django-forms-bootstrap#django-forms-bootstrap
	"""
	return field.field.widget.__class__.__name__.lower()


#@register.filter
#def trousands_k(nr):
#	try:
#		nr = int(nr)
#	except ValueError:
#		return nr
#	if nr > 1000000:
#		return str(nr // 1000000) + 'M'
#	if nr > 1000:
#		return str(nr // 1000) + 'k'
