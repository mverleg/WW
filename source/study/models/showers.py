from django.db import models

from study.models.profile import StudyProfile


class BaseShower(models.Model):
	"""
		Determines which enabled cards are asked next.

		Non-abstract base class for foreign keys.
	"""
	name = models.CharField(max_length = 48)
	profile = models.ForeignKey(StudyProfile)

	def next_question(self):
		"""
			Return the translation to ask about next.
		"""
		#todo (see selection.py)

	def _get_all_options(self):

		#todo (for use in next_question)

	#todo: think about this class' interface

	def get_score(self, learner, result, verified = False):
		"""
			Return the score change for a result.
		"""
		#todo (see score.py)


#todo: take into consideration that actives should be split to different profiles (rather than be used-based)
#todo: are score files also necessary? (e.g. could two selectors use the same card scores even though they possibly assign differently?)
#todo: should anything be split here? e.g. card activation from card selection from score assignment? related though

# there's a step active[*] -> currently learning[*]

class SimpleShower(BaseActivator):
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


