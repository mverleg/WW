
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
		if vote.up == up:
			vote.delete()
			add_message(request, INFO, 'Your vote for "%s" was removed.' % (translation.text))
		else:
			vote.up = up
			vote.save()
			add_message(request, INFO, 'Your vote for "%s" was changed from %s to %s.' % (translation.text, 'down' if up else 'up', 'up' if up else 'down'))
	else:
		vote = TranslationVote(translation = translation, up = up, learner = request.user)
		vote.save()
		add_message(request, INFO, 'Your vote for "%s" was added.' % (translation.text))
	return redirect(request.POST['next'] or translation.phrase.get_absolute_url())


@login_required
def add_translation_comment(request):
	return notification(request, 'Not implemented')


@login_required
def delete_translation_comment(request):
	return notification(request, 'Not implemented')


