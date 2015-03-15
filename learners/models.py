
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


"""
	Just ignore this for now.
"""
class LearnerManager(UserManager):

	def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
		email = self.normalize_email(email)
		user = self.model(email = email, is_staff = is_staff, is_superuser = is_superuser, **extra_fields)
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

	email = models.EmailField(blank = True, unique = True, max_length = 254, help_text = 'Email address; also used as login name.')
	name = models.CharField(max_length = 48, help_text = 'Visible name on the site.')
	is_staff = models.BooleanField(default = False, help_text = 'Designates whether the user can log into this admin site.')
	#language = models.CharField(choices = SUPPORTED_LANGUAGES, max_length = 8)

	ask_direction = models.FloatField(default = 65, validators = [MinValueValidator(0), MaxValueValidator(100)], help_text = 'How often to show the known language and ask the unknown one, versus the other way around (0: always show unknown, 100: always show known)')
	add_randomness = models.BooleanField(default = True, help_text = 'Should selecting phrases involve a little randomness?')
	minimum_delay = models.PositiveIntegerField(default = 10, help_text = 'For how many questions to block a phrase after displaying it.')
	new_count = models.PositiveIntegerField(default = 10, help_text = 'How many first-time cards to keep active at once.')
	show_medium_correctness = models.BooleanField(default = False, help_text = 'Besides correct and incorrect, show a third option inbetween them.')
	phrase_index = models.IntegerField(default = 0, help_text = 'How many phrases have been shown (a.o. to compare last_shown) (internal only)')
	need_active_update = models.BooleanField(default = True, help_text = 'Do the cache fields on active phrases need updating? (internal only)')

	objects = LearnerManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	class Meta:
		app_label = 'learners'

	def __unicode__(self):
		return self.get_short_name()

	def get_short_name(self):
		return self.name or '(nameless#%d)' % self.pk

	def need_update(self):
		self.need_active_update = True
		self.save()


