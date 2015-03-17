
from django.utils.translation import get_language, activate
from django.utils.translation import ugettext_lazy as _
from settings import SUPPORTED_LANGUAGES


def get_in_each_language(txt):
	txts = set()
	old_lang = get_language()
	for code, name in SUPPORTED_LANGUAGES:
		activate(code)
		txts.add(unicode(_(txt)))
	activate(old_lang)
	return txts


