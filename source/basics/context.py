
from study.models import Result


def statistics(request):
	correct_count = 0
	if request.user.is_authenticated():
		correct_count = Result.objects.filter(learner = request.user, result = Result.CORRECT).count()
	return {
		'correct_count': correct_count,
	}


