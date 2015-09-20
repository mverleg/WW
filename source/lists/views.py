
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, INFO, WARNING
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.forms import formset_factory, modelformset_factory
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from haystack.forms import HighlightedModelSearchForm
from basics.decorators import instantiate, confirm_first, next_GET
from basics.views import notification
from learners.forms import IdentifyUserByEmail
from lists.forms import ListForm, ListAccessForm, ListActivationForm
from lists.models import ListAccess, TranslationsList
from phrasebook.models import Translation


@instantiate(TranslationsList, in_kw_name = 'pk', out_kw_name = 'translations_list')
def show_list(request, translations_list, slug = None):
	access_instance = None
	try:
		# learner = request.user should work here, but it doesn't, so use request.user.id as a kind of hack
		# http://stackoverflow.com/questions/15878860/int-argument-must-be-a-string-or-a-number-not-simplelazyobject
		access_instance = ListAccess.objects.get(translations_list = translations_list, learner = request.user.id)
	except ListAccess.DoesNotExist:
		if not translations_list.public:
			return notification(request, 'No access for list "%s".' % translations_list)
	translations = translations_list.translations.all()
	paginator = Paginator(translations, 50)
	page = request.GET.get('page', 1)
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		return redirect('%s?page=1' % request.path)
	except EmptyPage:
		return redirect('%s?page=%d' % (request.path, paginator.num_pages))
	return render(request, 'show_list.html', {
		'list': translations_list,
		'access': access_instance,
		'editable': access_instance.editable if access_instance else False,
		'items': items,
		'nearby_pages': _nearby_pages(items),
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
		return list(range(1, items.paginator.num_pages + 1))
	if items.number <= 6:
		return list(range(1, 9)) + [None, items.paginator.num_pages, items.paginator.num_pages + 1]
	if items.number >= items.paginator.num_pages - 6:
		return [1, 2, None] + list(range(items.paginator.num_pages - 8, items.paginator.num_pages + 1))
	return [1, 2, None] + list(range(items.number - 2, items.number + 3)) + [None, items.paginator.num_pages, items.paginator.num_pages + 1]


def all_lists(request):
	public_lists = TranslationsList.objects.filter(public = True)
	paginator = Paginator(public_lists, 15)
	page = request.GET.get('page', 1)
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		return redirect('%s?page=1' % request.path)
	except EmptyPage:
		return redirect('%s?page=%d' % (request.path, paginator.num_pages))
	if request.user.is_authenticated():
		access_lists = [ac.translations_list for ac in ListAccess.objects.filter(translations_list__public = True, learner = request.user)]
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
		return redirect(li.get_absolute_url())
	return render(request, 'edit_list.html', {
		'list_form': list_form,
		'access_form': access_form,
		'add': True,
	})


@login_required
@instantiate(TranslationsList, in_kw_name = 'pk', out_kw_name = 'translations_list')
@next_GET
def edit_list(request, translations_list, slug = None, next = None):
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
			return redirect(request.POST['next'] or translations_list.get_absolute_url())
	else:
		if list_form.is_valid() and access_form.is_valid():
			access_form.save()
			return redirect(request.POST['next'] or translations_list.get_absolute_url())
	return render(request, 'edit_list.html', {
		'list_form': list_form,
		'access_form': access_form,
		'add': False,
		'list': translations_list,
		'access': access_instance,
		'next': next,
	})


@instantiate(TranslationsList, in_kw_name = 'pk', out_kw_name = 'translations_list')
@next_GET
def list_followers(request, translations_list, slug = None, next = None):
	editors = ListAccess.objects.filter(translations_list = translations_list, access = ListAccess.EDIT)
	followers = ListAccess.objects.filter(translations_list = translations_list, access = ListAccess.VIEW)

	try:
		access_instance = ListAccess.objects.get(translations_list = translations_list, learner = request.user)
	except ListAccess.DoesNotExist:
		pass
	form = IdentifyUserByEmail(request.POST or None)
	if form.is_valid():
		learner = form.instance
		if ListAccess.objects.filter(learner = learner, translations_list = translations_list).count():
			add_message(request, WARNING, 'the user with email "%s" already has access to this list.' % learner.email)
		else:
			access = ListAccess(learner = learner, translations_list = translations_list, access = ListAccess.VIEW)
			access.save()
			add_message(request, INFO, 'the user with email "%s" has been added!' % learner.email)
		return redirect(to = reverse('list_followers', kwargs = {'pk': translations_list.pk, 'slug': translations_list.slug}))
	return render(request, 'show_followers.html', {
		'list': translations_list,
		'editors': editors,
		'followers': followers,
		'current_access': access_instance,
		'user_form': form,
	})


@require_POST
@login_required
#@confirm_first(message = 'Are you sure you want to remove the privilege from this user?', submit_class = 'btn-danger')
def demote_follower(request):
	resp, li, access = _list_access_from_post_pk(request, request.POST, need_edit = True)
	if resp: return resp
	try:
		access = ListAccess.objects.get(pk = int(request.POST['access_pk']))
	except KeyError:
		return notification(request, 'No access key found.')
	except ValueError:
		return notification(request, 'Access key "%s" is not a valid format found.' % request.POST['access_pk'])
	except ListAccess.DoesNotExist:
		return notification(request, 'Access not found for key %s.' % request.POST['access_pk'])
	if access.access == ListAccess.EDIT:
		if ListAccess.objects.filter(translations_list = li, access = ListAccess.EDIT).count() <= 1:
			return notification(request, 'You cannot remove the last editor from a list.')
		access.access = ListAccess.VIEW
		access.save()
		add_message(request, INFO, '"%s" was demoted to a follower of the list.' % access.learner)
	elif access.access == ListAccess.VIEW:
		if li.public:
			return notification(request, 'You cannot remove followers from a public list.')
		access.delete()
		add_message(request, INFO, '"%s" was removed from the list.' % access.learner)
	else:
		raise AssertionError('unknown access state')
	return redirect(request.POST['next'] or reverse('list_followers', kwargs = {'pk': li.pk, 'slug': li.slug}))


@require_POST
@login_required
def promote_follower(request):
	resp, li, access = _list_access_from_post_pk(request, request.POST, need_edit = True)
	if resp: return resp
	try:
		access = ListAccess.objects.get(pk = int(request.POST['access_pk']))
	except KeyError:
		return notification(request, 'No access key found.')
	except ValueError:
		return notification(request, 'Access key "%s" is not a valid format found.' % request.POST['access_pk'])
	except ListAccess.DoesNotExist:
		return notification(request, 'Access not found for key %s.' % request.POST['access_pk'])
	if access.access == ListAccess.EDIT:
		return notification(request, 'User %s already has all privileges.' % access.learner)
	elif access.access == ListAccess.VIEW:
		access.access = ListAccess.EDIT
		access.save()
	else:
		raise AssertionError('unknown access state')
	add_message(request, INFO, '"%s" was promoted to editor of the list.' % access.learner)
	return redirect(request.POST['next'] or reverse('list_followers', kwargs = {'pk': li.pk, 'slug': li.slug}))


@require_POST
@login_required
def add_translation_by_search(request):
	resp, li, access = _list_access_from_post_pk(request, request.POST, need_edit = True)
	if resp: return resp
	form = HighlightedModelSearchForm(request.POST)
	if li.language:
		results = form.search().filter(language_key = li.language)
		other_language_results = form.search().filter(language_key__not = li.language)
	else:
		results = form.search()
		other_language_results = None
	if len(results) == 1:
		if results[0].language_key == li.language or li.language is None:
			""" Only one results, apply directly. """
			if results[0].object in li.translations.all():
				add_message(request, WARNING, '"%s" (the only result) is already on the list.' % results[0].object)
			else:
				li.translations.add(results[0].object)
				""" everyone who follows this list needs to update active translations """
				for need_update_access in ListAccess.objects.filter(translations_list = li):
					need_update_access.learner.need_update()
				add_message(request, INFO, '"%s" (the only result) was added to the list.' % results[0].object)
			return redirect(request.POST['next'] or li.get_absolute_url())
	""" Show options to the user """
	return render(request, 'add_choose.html', {
		'results': results,
		'language_results': other_language_results,
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
		""" everyone who follows this list needs to update active translations """
		for need_update_access in ListAccess.objects.filter(translations_list = li):
			need_update_access.learner.need_update()
		add_message(request, INFO, '"%s" was added to the list.' % translation)
	return redirect(request.POST['next'] or li.get_absolute_url())


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


@login_required
def remove_translation(request):
	resp, li, access = _list_access_from_post_pk(request, request.POST, need_edit = True)
	if resp: return resp
	try:
		translation = Translation.objects.get(pk = int(request.POST['trans_pk']))
	except KeyError:
		return notification(request, 'No translation key found.')
	except ValueError:
		return notification(request, 'Translation key "%s" is not a valid format found.' % request.POST['trans_pk'])
	except TranslationsList.DoesNotExist:
		return notification(request, 'Translation not found for key %s.' % request.POST['trans_pk'])
	li.translations.remove(translation)
	add_message(request, INFO, '"%s" was removed from the list.' % translation)
	return redirect(request.POST['next'] or li.get_absolute_url())


@login_required
@require_POST
@confirm_first(message = 'Are you sure you want to delete this list? Please consider handing control of the list to someone else if you\'ve lost interest but it could still be of use.', submit_class = 'btn-danger')
def delete_list(request):
	resp, li, access = _list_access_from_post_pk(request, request.POST, need_edit = True)
	if resp: return resp
	if ListAccess.objects.filter(translations_list = li, access = ListAccess.EDIT).count() > 1:
		return notification(request, 'There are other editors for this list. This means you cannot delete it. Unfollow it instead.')
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
	add_message(request, INFO, 'You are now following the list "%s".' % li)
	return redirect(request.POST['next'] or li.get_absolute_url())


@login_required
@require_POST
@confirm_first(message = 'Are you sure you want to unfollow this list? You can only refollow it if it\'s a public list.', submit_class = 'btn-danger')
def unfollow_list(request):
	#todo: only confirm if it's not public
	resp, li, access = _list_access_from_post_pk(request, request.POST, need_access = True, need_edit = False)
	if resp: return resp
	if access.access == ListAccess.EDIT:
		return notification(request, 'You are an editor for this list, you cannot unfollow it. First go to the followers page and hand over editorship. Or delete the list if you\re sure it\'s of no use to anyone.')
	access.delete()
	return redirect(request.POST['next'] or reverse('all_lists'))


@login_required
def list_activities(request):
	list_accesses = ListAccess.objects.filter(learner = request.user).order_by('-active', '-priority')
	FormFac = modelformset_factory(ListAccess, form = ListActivationForm, extra = 0)
	forms = FormFac(request.POST or None, queryset = list_accesses)
	next = request.GET.get('next', request.POST.get('next', ''))
	if forms.is_valid():
		forms.save()
		add_message(request, INFO, 'Your lists have been updated')
		if next:
			return redirect(to = '{0:s}?next={1:s}'.format(reverse('list_activities'), next))
		return redirect(to = reverse('list_activities'))
	return render(request, 'activations.html', {
		'forms': forms,
		'next': next,
	})


