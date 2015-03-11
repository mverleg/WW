
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, INFO, WARNING
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from haystack.forms import HighlightedModelSearchForm
from basics.decorators import instantiate, confirm_delete, confirm_first
from basics.views import notification
from lists.forms import ListForm, ListAccessForm
from lists.models import ListAccess, TranslationsList
from phrasebook.models import Translation


@instantiate(TranslationsList, in_kw_name = 'pk', out_kw_name = 'translations_list')
def show_list(request, translations_list, slug = None):
	try:
		access_instance = ListAccess.objects.get(translations_list = translations_list, learner = request.user)
	except ListAccess.DoesNotExist:
		if not translations_list.public:
			return notification(request, 'No access for list "%s".' % translations_list)
		access_instance = {'editable': False}
	translations = translations_list.translations.all()
	#todo: pagination (only load translations on page, for performance)
	return render(request, 'show_list.html', {
		'list': translations_list,
		'translations': translations,
		'access': access_instance,
	})


def user_lists(request):
	if not request.user.is_authenticated():
		add_message(request, INFO, 'You can\'t manage your own lists yet. First register or login.')
		return redirect(reverse('all_lists'))
	edit_accesses = ListAccess.objects.filter(learner = request.user, access = ListAccess.EDIT)
	view_accesses = ListAccess.objects.filter(learner = request.user, access = ListAccess.VIEW)
	return render(request, 'user_lists.html', {
		'edit_accesses': edit_accesses,
		'view_accesses': view_accesses,
	})


def _nearby_pages(items):
	"""
		Get a list of pages to display for pagination, and None values for continuation dots.

		Shows up to 12 values, always shows the fist and last two elements and the two elements left and right of the current one.
	"""
	if items.paginator.num_pages <= 10:
		return range(1, items.paginator.num_pages + 1)
	if items.number <= 6:
		return range(1, 9) + [None, items.paginator.num_pages, items.paginator.num_pages + 1]
	if items.number >= items.paginator.num_pages - 6:
		return [1, 2, None] + range(items.paginator.num_pages - 8, items.paginator.num_pages + 1)
	return [1, 2, None] + range(items.number - 2, items.number + 3) + [None, items.paginator.num_pages, items.paginator.num_pages + 1]


def all_lists(request):
	#todo: hide own lists (or at least hide follow button)
	public_lists = TranslationsList.objects.filter(public = True)
	paginator = Paginator(public_lists, 15)
	page = request.GET.get('page', 1)
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		return redirect('%s?page=1' % request.path)
	except EmptyPage:
		return redirect('%s?page=%d' % (request.path, paginator.num_pages))
	access_lists = [ac.translations_list for ac in ListAccess.objects.filter(translations_list__public = True)]
	for li in items.object_list:
		if li in access_lists:
			li.following = True
	return render(request, 'all_lists.html', {
		'items': items,
		'nearby_pages': _nearby_pages(items),
	})


@login_required
def add_list(request):
	list_form = ListForm(request.POST or None)
	access_form = ListAccessForm(request.POST or None)
	if list_form.is_valid() and access_form.is_valid():
		""" Create the list and grant the user edit access """
		li = list_form.save()
		access = access_form.save(commit = False)
		access.translations_list = li
		access.learner = request.user
		access.access = ListAccess.EDIT
		access.save()
		return redirect(reverse('show_list', kwargs = {'pk': li.pk, 'slug': li.slug}))
	return render(request, 'edit_list.html', {
		'list_form': list_form,
		'access_form': access_form,
		'add': True,
	})


@login_required
@instantiate(TranslationsList, in_kw_name = 'pk', out_kw_name = 'translations_list')
def edit_list(request, translations_list, slug = None):
	list_form = ListForm(request.POST or None, instance = translations_list)
	try:
		access_instance = ListAccess.objects.get(translations_list = translations_list, learner = request.user)
	except ListAccess.DoesNotExist:
		return notification(request, 'No access for list "%s".' % translations_list)
	access_form = ListAccessForm(request.POST or None, instance = access_instance)
	if access_instance.editable:
		if list_form.is_valid() and access_form.is_valid():
			list_form.save()
			access_form.save()
			return redirect(reverse('show_list', kwargs = {'pk': translations_list.pk, 'slug': translations_list.slug}))
	else:
		if list_form.is_valid() and access_form.is_valid():
			access_form.save()
			return redirect(reverse('show_list', kwargs = {'pk': translations_list.pk, 'slug': translations_list.slug}))
	return render(request, 'edit_list.html', {
		'list_form': list_form,
		'access_form': access_form,
		'add': False,
		'list': translations_list,
		'access': access_instance,
	})


@require_POST
@login_required
def add_translation_by_search(request):
	resp, li, access = _list_access_from_post_pk(request, request.POST, need_edit = True)
	if resp: return resp
	form = HighlightedModelSearchForm(request.POST)
	if li.language:
		results = form.search().filter(language = li.language)
	else:
		results = form.search()
	if len(results) == 1:
		""" Only one results, apply directly. """
		if results[0].object in li.translations.all():
			add_message(request, WARNING, '"%s" (the only result) is already on the list.' % results[0].object)
		else:
			li.translations.add(results[0].object)
			add_message(request, INFO, '"%s" (the only result) was added to the list.' % results[0].object)
		return redirect(request.POST['next'] or reverse('show_list', kwargs = {'pk': li.pk, 'slug': li.slug}))
	else:
		""" Show options to the user """
		return render(request, 'add_choose.html', {
			'results': results,
			'query': request.POST['q'],
			'list': li,
			'next': request.POST['next'],
		})


@login_required
@instantiate(Translation, in_kw_name = 'pk', out_kw_name = 'translation')
def add_translation_by_pk(request, translation):
	resp, li, access = _list_access_from_post_pk(request, request.POST, need_edit = True)
	if resp: return resp
	if translation in li.translations.all():
		add_message(request, WARNING, '"%s" is already on the list.' % translation)
	else:
		li.translations.add(translation)
		add_message(request, INFO, '"%s" was added to the list.' % translation)
	return redirect(request.POST['next'] or reverse('show_list', kwargs = {'pk': li.pk, 'slug': li.slug}))


def _list_access_from_post_pk(request, post, need_access = True, need_edit = True):
	"""
		:return: response, list, access (either the first or the other two are None)
	"""
	if not need_access: need_edit = False
	try:
		list_instance = TranslationsList.objects.get(pk = int(request.POST['pk']))
	except KeyError:
		return notification(request, 'No list key found.'), None, None
	except ValueError:
		return notification(request, 'List key "%s" is not a valid format found.' % request.POST['pk']), None, None
	except TranslationsList.DoesNotExist:
		return notification(request, 'List not found for key %s.' % request.POST['pk']), None, None
	try:
		access_instance = ListAccess.objects.get(translations_list = list_instance, learner = request.user)
	except ListAccess.DoesNotExist:
		if need_access:
			return notification(request, 'No access for list "%s".' % list_instance), None, None
		else:
			access_instance = None
	if need_edit:
		if not access_instance.access == ListAccess.EDIT:
			return notification(request, 'You don\'t have edit access for list %s.' % list_instance), None, None
	return None, list_instance, access_instance


@confirm_delete
@login_required
@require_POST
def delete_list(request):
	resp, li, access = _list_access_from_post_pk(request, request.POST, need_edit = True)
	if resp: return resp
	li.delete()
	return redirect(reverse('user_lists'))


@login_required
@require_POST
def follow_list(request):
	resp, li, access = _list_access_from_post_pk(request, request.POST, need_access = False)
	if resp: return resp
	if access:
		return notification(request, 'You are already following the list "%s"' % li.name)
	ListAccess(access = ListAccess.VIEW, translations_list = li, learner = request.user).save()
	add_message(request, INFO, 'You are not following the list "%s".' % li)
	return redirect(request.POST['next'] or reverse('show_list', kwargs = {'pk': li.pk, 'slug': li.slug}))


@login_required
@require_POST
@confirm_first(message = 'Are you sure you want to unfollow this list? You can only refollow it if it\'s a public list.', submit_class = 'btn-danger')
def unfollow_list(request):
	resp, li, access = _list_access_from_post_pk(request, request.POST, need_access = True, need_edit = False)
	if resp: return resp
	access.delete()
	return redirect(request.POST['next'] or reverse('show_list', kwargs = {'pk': li.pk, 'slug': li.slug}))


