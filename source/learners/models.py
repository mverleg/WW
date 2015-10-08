
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


