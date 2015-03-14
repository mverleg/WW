
from django.db import models
from learners.models import Learner
from phrasebook.models import Translation
from settings import SUPPORTED_LANGUAGES


class Result(models.Model):
	CORRECT, INCORRECT, CLOSE = 'good', 'bad', 'kinda'
	learner = models.ForeignKey(Learner)
	translation = models.ForeignKey(Translation)
	language = models.CharField(choices = SUPPORTED_LANGUAGES, max_length = 8)
	result = models.CharField(choices = (
		(CORRECT, 'correct'),
		(INCORRECT, 'incorrect'),
		(CLOSE, 'not quite correct'),
	), max_length = 12)


