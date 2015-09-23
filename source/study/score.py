
from study.models import Result, ActiveTranslation


def update_score(learner, result, verified = False):
	"""
		Update the score after a phrase has been judged.

		:param result: Result.CORRECT, Result.CLOSE or Result.INCORRECT
		:return: Result instance
	"""
	if result == Result.CORRECT:
		base = learner.reward_magnitude
	elif result == Result.CLOSE:
		base = - learner.reward_magnitude
	elif result == Result.INCORRECT:
		base = -2 * learner.reward_magnitude
	else:
		raise Exception('Scoring does not know how to deal with result = %s' % result)
	learner.study_active.score += base
	#todo: take history into account: the same phrase correct 5 times in a row should increase score a lot (don't show again) [actually independent of new result: many correct before should amplify result]
	#if learner.study_show_learn:
	#	judge_translation = learner.study_shown
	#else:
	#	judge_translation = learner.study_hidden
	#print judge_translation.language
	#try:
	#	active = ActiveTranslation.objects.get(learner = learner, translation = judge_translation)
	#except ActiveTranslation.DoesNotExist:
	#	raise ActiveTranslation.DoesNotExist('The ActiveTranslation with learner="%s" translation="%" (%s) was not found while assigning scores. This means it disappeared between asking the question and answering it (they shouldn\'t disappear) or that the algorithm doesn\'t recover it correctly')
	#if not judge_translation.language == request.LEARN_LANG:
	#	stderr.write('the translation to which score will be assigned is not in the learning langauge')
	result = Result(
		learner = learner,
		asked = learner.study_hidden,
		known = learner.study_shown,
		result = result,
		verified = False
	)
	learner.study_active.save()
	result.save()
	return result


