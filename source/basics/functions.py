
from django.utils.translation import get_language, activate
from django.utils.translation import ugettext_lazy as _
from settings import SUPPORTED_LANGUAGES
from xpinyin import Pinyin


xpinyin = Pinyin()


def get_in_each_language(txt):
	txts = set()
	old_lang = get_language()
	for code, name in SUPPORTED_LANGUAGES:
		activate(code)
		txts.add(str(_(txt)))
	activate(old_lang)
	return txts


def to_pinyin(cny):
	return xpinyin.get_pinyin(cny, splitter=' ', show_tone_marks=False)


