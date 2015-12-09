
from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from django.utils.translation import get_language
from study.functions import make_default_profile
from study.models.activators import PriorityLimitedActivator
from study.models.display_selector import DisplayMode, DisplayRandomSelector, DisplayRandomMode
from study.models.phrase_chooser import SimplePhraseChooser
from study.models.profile import StudyProfile
from study.models.scorers import LinearScorer


class LearnerManager(UserManager):
	"""
	Manages queries for Learner; mostly makes sure that new users have a profile.
	"""
	def _create_user_with_profile(self, email, password, is_staff, is_superuser,
			learn_language=settings.DEFAULT_LEARN_LANGUAGE, known_language=None, **extra_fields):
		if known_language is None:
			known_language = get_language()
		email = self.normalize_email(email)
		user = self.model(email=email, is_staff=is_staff, is_superuser=is_superuser, last_login=now(), **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		profile = make_default_profile(learner=user, learn_language=learn_language, known_language=known_language)
		user.active_profile = profile
		user.save()
		return user

	def create_user(self, email, password=None, **extra_fields):
		return self._create_user_with_profile(email=email, password=password, is_staff=False, is_superuser=False, **extra_fields)

	def create_nologin_user(self, email, **extra_fields):
		user = self._create_user_with_profile(email=email, is_staff=False, is_superuser=False, **extra_fields)
		user.set_unusable_password()
		return user

	def create_superuser(self, email, password, **extra_fields):
		return self._create_user_with_profile(email=email, password=password, is_staff=True, is_superuser=True, **extra_fields)


class Learner(AbstractBaseUser, PermissionsMixin):
	"""
	This is the learner. Their email is their username and they get a password.
	"""
	email = models.EmailField(blank=True, unique=True, max_length=254,
		help_text='Email address; also used as login name.')
	name = models.CharField(max_length=48, help_text='Visible name on the site.')
	is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')

	active_profile = models.ForeignKey(StudyProfile, null=True, blank=False, related_name='active_for_learner')

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


