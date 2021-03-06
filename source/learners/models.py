
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now

"""
	Just ignore this for now.
"""
class LearnerManager(UserManager):

	def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
		email = self.normalize_email(email)
		user = self.model(email = email, is_staff = is_staff, is_superuser = is_superuser, last_login = now(), **extra_fields)
		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_user(self, email, password = None, **extra_fields):
		return self._create_user(email = email, password = password, is_staff = False, is_superuser = False, **extra_fields)

	def create_nologin_user(self, email, **extra_fields):
		user = self._create_user(email = email, is_staff = False, is_superuser = False, **extra_fields)
		user.set_unusable_password()
		return user

	def create_superuser(self, email, password, **extra_fields):
		return self._create_user(email = email, password = password, is_staff = True, is_superuser = True, **extra_fields)


"""
	This is the learner. Their email is their username and they get a password. Ignore the details for now.
"""
class Learner(AbstractBaseUser, PermissionsMixin):

	""" Account details """
	email = models.EmailField(blank = True, unique = True, max_length = 254, help_text = 'Email address; also used as login name.')
	name = models.CharField(max_length = 48, help_text = 'Visible name on the site.')
	is_staff = models.BooleanField(default = False, help_text = 'Designates whether the user can log into this admin site.')

	""" Settings """
	ask_direction = models.FloatField(default = 65, validators = [MinValueValidator(0), MaxValueValidator(100)], help_text = 'How often to show the known language and ask the unknown one, versus the other way around (0: always show unknown, 100: always show known).')
	#add_randomness = models.BooleanField(default = True, help_text = 'Should selecting phrases involve a little randomness?')
	minimum_delay = models.PositiveIntegerField(default = 10, help_text = 'For how many questions to block a phrase after displaying it.')
	new_count = models.PositiveIntegerField(default = 10, help_text = 'How many unlearned translations to keep active at once.')
	show_medium_correctness = models.BooleanField(default = False, help_text = 'Besides correct and incorrect, show a third option inbetween them.')
	show_correct_count = models.BooleanField(default = True, help_text = 'Show the number of correct responses on every page.')
	reward_magnitude = models.IntegerField(default = 10, help_text = 'Indicates the base magnitude or increase or decrease for a phrase\'s score when correct or incorrect.')
	favor_unknown = models.FloatField(default = 10, validators = [MinValueValidator(0), MaxValueValidator(100)], help_text = 'A higher value makes unknown phrases more likely to appear during study sessions, relative to known ones.')

	""" Internal bookkeeping """
	NOTHING, ASKING, REVEALED, JUDGED = 0, 1, 3, 4  # 2 missing for historical reasons
	phrase_index = models.PositiveIntegerField(default = 100, help_text = 'How many phrases have been shown (a.o. to compare last_shown) (internal only).')
	need_active_update = models.BooleanField(default = True, help_text = 'Do the cache fields on active phrases need updating? (internal only).')
	study_shown = models.ForeignKey('phrasebook.Translation', blank = True, null = True, default = None, related_name = 'current_shown_learners', help_text = 'The Translation that is currently visible, if any (internal only).')
	study_hidden = models.ForeignKey('phrasebook.Translation', blank = True, null = True, default = None, related_name = 'current_hidden_learners', help_text = 'The Translation that is the solution for study_shown (internal only).')
	study_answer = models.TextField(default = '', blank = True, help_text = 'The latest thing the user answered (internal only).')
	study_active = models.ForeignKey('study.ActiveTranslation', blank = True, null = True, related_name = 'current_learners', help_text = 'The current ActiveTranslation that is being asked and for which scores should be assigned.')
	study_state = models.PositiveSmallIntegerField(default = NOTHING, choices = (
		(NOTHING, 'nothing'),
		(ASKING, 'asking meaning (showing learn lang)'),
		(REVEALED, 'revealed, awaiting judgement'),
		(JUDGED, 'judged')
	), help_text = '(internal only).')


	objects = LearnerManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	class Meta:
		app_label = 'learners'

	def __str__(self):
		return self.get_short_name()

	def get_short_name(self):
		return self.name or '(nameless#%d)' % self.pk

	def need_update(self):
		self.need_active_update = True
		self.save()


