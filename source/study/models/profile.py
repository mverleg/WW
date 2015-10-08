
from operator import itemgetter
from random import random
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class StudyProfile(models.Model):
	"""
		Contains the study settings for a user, so the user can easy switch between study methods.
	"""
	ask_direction = models.FloatField(default = 65, validators = [MinValueValidator(0), MaxValueValidator(100)], help_text = 'How often to show the known language and ask the unknown one, versus the other way around (0: always show unknown, 100: always show known).')
	#add_randomness = models.BooleanField(default = True, help_text = 'Should selecting phrases involve a little randomness?')
	minimum_delay = models.PositiveIntegerField(default = 10, help_text = 'For how many questions to block a phrase after displaying it.')
	new_count = models.PositiveIntegerField(default = 10, help_text = 'How many unlearned translations to keep active at once.')
	show_medium_correctness = models.BooleanField(default = False, help_text = 'Besides correct and incorrect, show a third option inbetween them.')
	show_correct_count = models.BooleanField(default = True, help_text = 'Show the number of correct responses on every page.')
	reward_magnitude = models.IntegerField(default = 10, help_text = 'Indicates the base magnitude or increase or decrease for a phrase\'s score when correct or incorrect.')
	favor_unknown = models.FloatField(default = 10, validators = [MinValueValidator(0), MaxValueValidator(100)], help_text = 'A higher value makes unknown phrases more likely to appear during study sessions, relative to known ones.')

	NOTHING, ASKING, REVEALED, JUDGED = 0, 1, 3, 4  # 2 missing for historical reasons
	phrase_index = models.PositiveIntegerField(default = 100, help_text = 'How many phrases have been shown (a.o. to compare last_shown) (internal only).')
	need_active_update = models.BooleanField(default = True, help_text = 'Do the cache fields on active phrases need updating? (internal only).')
	study_shown = models.ForeignKey('phrasebook.Translation', blank = True, null = True, default = None, related_name = 'current_shown_learners', help_text = 'The Translation that is currently visible, if any (internal only).')
	study_hidden = models.ForeignKey('phrasebook.Translation', blank = True, null = True, default = None, related_name = 'current_hidden_learners', help_text = 'The Translation that is the solution for study_shown (internal only).')
	study_answer = models.TextField(default = '', blank = True, help_text = 'The latest thing the user answered (internal only).')
	#todo: move study_active and others to card_shower
	study_active = models.ForeignKey('study.ActiveTranslation', blank = True, null = True, related_name = 'current_learners', help_text = 'The current ActiveTranslation that is being asked and for which scores should be assigned.')
	study_state = models.PositiveSmallIntegerField(default = NOTHING, choices = (
		(NOTHING, 'nothing'),
		(ASKING, 'asking meaning (showing learn lang)'),
		(REVEALED, 'revealed, awaiting judgement'),
		(JUDGED, 'judged')
	), help_text = '(internal only).')

	#todo: prefetch related (at least specific ones)




