"""
	Settings file

	You can set the database settings in here at DATABASES['default']

	You can also set the supported languages with SUPPORTED_LANGUAGES

	Before you launch the site, you should probably set DATABASE password and the SECRET_KEY to something that
	is not in a public git repository...
"""

from django.utils.translation import ugettext_lazy as _
from os.path import join, dirname
import sys


SUPPORTED_LANGUAGES = (
	# the first is language key / database value (max 8 chars, don't change), the second is the display name
	('en-gb', _('English (British)')),
	('zh-cn', _('Chinese (simplified Mandarin)')),
	('de', _('German')),
	('nl', _('Dutch')),
)
#SUPPORTED_LANGUAGES = DEFAULT_LANGUAGES  # replace this if you want to limit the available languages
DEFAULT_KNOWN_LANGUAGE = 'zh-cn'
DEFAULT_LEARN_LANGUAGE = 'nl'

# Build paths inside the project like this: join(BASE_DIR, ...)
BASE_DIR = dirname(__file__)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=)z3(+)z!jaizz^$ggqme0q)49vy2qs-9g+5@h&340qopx^$4w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'learners.Learner'

# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'haystack',
	'basics',
	'learners',
	'phrasebook',
	'lists',
	'study',
	'opinions',
	'importing',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.locale.LocaleMiddleware',   # should be after SessionMiddleware
	'basics.middleware.SetLearningLanguage'  # should be after LocaleMiddleWare
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'django.core.context_processors.tz',
	'django.contrib.messages.context_processors.messages',
	'django.core.context_processors.request',
	'basics.context.statistics',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': join(BASE_DIR, 'database.sqlite3'),
	},
	## reaplce with this to us mySQL (make sure the database is UTF8):
	#'default': {
	#	'ENGINE': 'django.db.backends.mysql',
	#	'NAME': 'words_database',
	#	'USER': 'werner',
	#	'PASSWORD': 'Wx3G4fqABzwZZAz',
	#	'HOST': '127.0.0.1',
	#	'PORT': '',
	#}
}

LOGIN_URL = '/learner/login/'
LOGIN_REDIRECT_URL = '/learner/profile/'

PREPEND_WWW = False  # I like turning this on for real sites, but it doesn't work if you access the site using an IP (like 127.0.0.1), so turn it on after testing
APPEND_SLASH = True

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGES = SUPPORTED_LANGUAGES
LANGUAGE_CODE = DEFAULT_LEARN_LANGUAGE
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (join(BASE_DIR, 'basics/locale/'),)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR, 'media')

TEMPLATE_DIRS = (
	join(BASE_DIR,  'templates'),
)

# search engine
# http://django-haystack.readthedocs.org/en/latest/tutorial.html
# should probably be changed once performance becomes an issue
HAYSTACK_CONNECTIONS = {
	'default': {
		'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
		'PATH': join(BASE_DIR, 'searchindex.whoosh'),
	},
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

try:
	from local import *
except ImportError:
	sys.stdout.write('created local.py settings directory')
	with open(join(BASE_DIR, 'local.py'), 'w+') as fh:
		fh.write('# store your local settings here (e.g. database)')


