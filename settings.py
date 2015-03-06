"""
	Settings file

	You can set the database settings in here at DATABASES['default']

	You can also set the supported languages with SUPPORTED_LANGUAGES

	Before you launch the site, you should probably set DATABASE password and the SECRET_KEY to something that
	is not in a public git repository...
"""

SUPPORTED_LANGUAGES = (
	# the first is a database key (max 8 chars), the second is the display name
	('en-gb', 'English (British)'),
	('zh', 'Mandarin Chinese'),
	('de', 'German'),
)
DEFAULT_LANGUAGE = SUPPORTED_LANGUAGES[0][0]

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)


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
	'basics',
	'learners',
	'phrasebook',
	'lists',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'basics.middleware.SetLearningLanguage',
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
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'database.sqlite3'),
	},
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

PREPEND_WWW = not DEBUG
APPEND_SLASH = True

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
	os.path.join(BASE_DIR,  'templates'),
)