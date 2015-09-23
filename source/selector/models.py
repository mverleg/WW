
from django.db import models


class BaseSelector(models.Model):
	"""
		Non-abstract base class for foreign keys.
	"""
	#todo: make auto-upgrade
	pass


#todo: take into consideration that actives should be split to different profiles (rather than be used-based)
#todo: are score files also necessary? (e.g. could two selectors use the same card scores even though they possibly assign differently?)
#todo: should anything be split here? e.g. card activation from card selection from score assignment? related though

class DemoSelector(BaseSelector):
	#todo: how to deal with selector-specific settings?

	def update_actives(self):
		"""
			Called when lists are (de)activated or when phrases are added to them.
		"""
		#todo: make sure this is called
		#todo: should this be two functions (like study/functions) or one?

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
			Return the score change for a result
		"""
		#todo (see score.py)


