
from django.db import models
from model_utils.managers import InheritanceManager
from phrasebook.models import Translation
from study.models.scorers import BaseScorer


class ActiveTranslation(models.Model):
	"""
	A user has a set of active phrases he is currently learning - he can limit the number of new ones.
	The phrases all have a score that is based on correct/incorrect answers (and possibly more);
	the lowest score phrase is asked next unless shown too recently.
	"""
	scorer = models.ForeignKey(BaseScorer)
	direction = models.IntegerField()
	translation = models.ForeignKey(Translation)
	last_shown = models.PositiveIntegerField()
	""" Note that score, active and priority are derived properties, stored for performance; it can be recalculated from other data. """
	score = models.FloatField(db_column = 'CACHE_score')  #todo: split into types depending on what's shown
	priority = models.SmallIntegerField(default = 0, db_column = 'CACHE_priority')
	active = models.BooleanField(default = False, db_column = 'CACHE_active')  # todo: maybe prefix _ since it's a change-like field

	# def update(self):
	# 	"""
	# 		Call to update the derived attributes.
	# 	"""
	# 	#todo: is this desirable?
	# 	#todo: make sure this is called
	# 	#see update_learner_actives

	class Meta:
		unique_together = ('scorer', 'translation',)
		ordering = ('score',)

	def __str__(self):
		return 'active "%s" for "%s"' % (self.translation, self.learner)


class BaseActivator(models.Model):
	"""
	Determines which cards from enabled lists are activated next.

	Non-abstract base class for foreign keys.
	"""
	#todo: could be expanded to suggest things like adding complements, examples, etc. when a phrase is activated
	#todo: make auto-upgrade
	#todo: how to deal with selector-specific settings?
	name = models.CharField(max_length = 48)
	profile = models.ForeignKey('study.StudyProfile')

	objects = InheritanceManager()

	def update_actives(self):
		"""
			Called when lists are (de)activated, when phrases are added to them or when score is updated (or for reset).
		"""
		#todo: make sure this is called
		#todo: should this be two functions (like study/functions) or one?


class PriorityLimitedActivator(models.Model):
	"""
	Simply activates the highest priority inactive translations until enough translations are active.
	"""
	bla = 0 #todo



#todo: perhaps some scoring settings should be in yet another instance
#todo: take into consideration that actives should be split to different profiles (rather than be used-based)
#todo: are score files also necessary? (e.g. could two selectors use the same card scores even though they possibly assign differently?)
#todo: should anything be split here? e.g. card activation from card selection from score assignment? related though

# there's a step active[*] -> currently learning[*]

class SimpleSelector(BaseActivator):
	"""
	???
	"""
	#todo: how to deal with selector-specific settings?

	def _get_all_actives(self):
		pass

	def update_actives(self):
		"""
			Called when lists are (de)activated or when phrases are added to them.
		"""
		pass

	def next_question(self):
		"""
			Return the translation to ask about next.
		"""
		#todo (see selection.py)

	def _get_all_options(self):
		pass
		#todo (for use in next_question)

	#todo: think about this class' interface

	def get_score(self, learner, result, verified = False):
		"""
			Return the score change for a result.
		"""
		#todo (see score.py)


