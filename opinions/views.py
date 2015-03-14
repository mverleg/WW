
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, INFO, WARNING, ERROR
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from basics.views import notification
from opinions.models import TranslationVote
from phrasebook.models import Translation


@login_required
@require_POST
def add_translation_vote(request):
	try:
		translation = Translation.objects.get(pk = int(request.POST['trans_pk']))
		votes = TranslationVote.objects.filter(learner = request.user, translation = translation)
		up = bool(int(request.POST['up']))
	except (KeyError, ValueError, Translation.DoesNotExist):
		return notification(request, message = 'The submitted data was not valid - translation and/or vote type were specified wrongly or not at all.')
	if votes:
		vote = votes[0]
		if not vote.up == up:
			vote.up = up
			vote.save()
			add_message(request, INFO, 'Your vote for "%s" was changed from %s to %s.' % (translation.text, 'down' if up else 'up', 'up' if up else 'down'))
		else:
			add_message(request, WARNING, 'Your vote for "%s" was ignored because you have already voted for it.' % (translation.text))
	else:
		vote = TranslationVote(translation = translation, up = up, learner = request.user)
		vote.save()
		add_message(request, INFO, 'Your vote for "%s" was added.' % (translation.text))
	return redirect(request.POST['next'] or reverse('show_phrase', kwargs = {'pk': translation.phrase.pk}))


@login_required
@require_POST
def delete_translation_vote(request):
	try:
		translation = Translation.objects.get(pk = int(request.POST['trans_pk']))
		votes = TranslationVote.objects.filter(learner = request.user, translation = translation)
	except (KeyError, ValueError, Translation.DoesNotExist):
		return notification(request, message = 'The submitted data was not valid - translation was specified wrongly or not at all.')
	except TranslationVote.DoesNotExist:
		add_message(request, ERROR, 'You have no votes for "%s", so they can\'t be removed.' % (translation.text))
		return redirect(request.POST['next'] or reverse('show_phrase', kwargs = {'pk': translation.phrase.pk}))
	votes[0].delete()
	add_message(request, INFO, 'Your vote for "%s" was removed.' % (translation.text))
	return redirect(request.POST['next'] or reverse('show_phrase', kwargs = {'pk': translation.phrase.pk}))


@login_required
def add_translation_comment(request):
	return notification(request, 'Not implemented')


@login_required
def delete_translation_comment(request):
	return notification(request, 'Not implemented')


