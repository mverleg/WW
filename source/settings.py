"""
	Settings file

	You can set the database settings in here at DATABASES['default']

	You can also set the supported languages with SUPPORTED_LANGUAGES

	Before you launch the site, you should probably set DATABASE password and the SECRET_KEY to something that
	is not in a public git repository...
"""

from random import SystemRandom
from django.utils.translation import ugettext_lazy as _
from os.path import join, dirname, exists
import string
import sys


SUPPORTED_LANGUAGES = (
	# the first is language key / database value (max 8 chars, don't change), the second is the display name
	('en-gb', _('English (British)')),
	('zh-cn', _('Chinese (simplified Mandarin)')),
	('he', _('Hebrew')),
	('de', _('German')),
	('nl', _('Dutch')),
)
#SUPPORTED_LANGUAGES = DEFAULT_LANGUAGES  # replace this if you want to limit the available languages
# DEFAULT_KNOWN_LANGUAGE = 'en-gb' # removed because it's always the user language
DEFAULT_LEARN_LANGUAGE = 'en-gb'

# Build paths inside the project like this: join(BASE_DIR, ...)
BASE_DIR = dirname(dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=)z3(+)z!jaizz^$ggqme0q)49vy2qs-9g+5@h&340qopx^$4w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
	'crispy_forms',
	'haystack',
	'avem_theme',
	'basics',
	'learners',
	'phrasebook',
	'lists',
	'study',
	'opinions',
	'importing',
)

# use django_extensions if it's installed
try:
	import django_extensions
except ImportError:
	pass
else:
	INSTALLED_APPS = ('django_extensions',) + INSTALLED_APPS

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

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				# Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
				# list if you haven't customized them:
				'django.contrib.auth.context_processors.auth',
				'django.template.context_processors.debug',
				'django.template.context_processors.i18n',
				'django.template.context_processors.media',
				'django.template.context_processors.static',
				'django.template.context_processors.tz',
				'django.contrib.messages.context_processors.messages',
				'django.core.context_processors.request',
				'basics.context.statistics',
			],
		},
	},
]
CRISPY_TEMPLATE_PACK = 'bootstrap3'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': join(BASE_DIR, 'data', 'database.sqlite3'),
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
LOCALE_PATHS = (join(BASE_DIR, 'locale'),)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR, 'media')

# search engine
# http://django-haystack.readthedocs.org/en/latest/tutorial.html
# should probably be changed once performance becomes an issue
HAYSTACK_CONNECTIONS = {
	'default': {
		'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
		'PATH': join(BASE_DIR, 'data', 'searchindex.whoosh'),
	},
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
		'LOCATION': '127.0.0.1:11211',
	}
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

try:
	if not exists(join(BASE_DIR, 'source', 'local.py')):
		with open(join(BASE_DIR, 'source', 'local.py'), 'w+') as fh:
			fh.write('"""\nLocal (machine specific) settings that overwrite the general ones.\n"""\n\n')
			fh.write('from os.path import join, realpath, dirname\n\n\n')
			fh.write('BASE_DIR = dirname(dirname(realpath(__file__)))\n\n')
			fh.write('DATABASES = {\'default\': {\n\t\'ENGINE\': \'django.db.backends.sqlite3\',\n\t\'NAME\': join(BASE_DIR, \'data\', \'aqua.db\'),\n}}\n\n')
			fh.write('ALLOWED_HOSTS = [\'localhost\', \'.localhost.markv.nl\',]\n\n')
			fh.write('SECRET_KEY = "{0:s}"\n\n'.format(''.join(SystemRandom().choice(string.ascii_letters + string.digits + '#$%&()*+,-./:;?@[]^_`{|}~') for _ in range(50))))
			fh.write('NOTIFICATION_PATH = join(BASE_DIR, \'notification.html\')\n\n')
			fh.write('DEBUG = True\n\n\n')
except Exception as err:
	print('could not create local.py settings file: {0:s}'.format(str(err)))

from local import *


