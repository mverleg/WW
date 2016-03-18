from re import split
from urllib.request import build_opener

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render
from basics.views import notification
from importing.forms import ImportForm, ChinesepodForm, TextForm
from lists.models import TranslationsList, ListAccess
from phrasebook.models import Phrase
from phrasebook.models import Translation


CNY, EN = 'zh-cn', 'en-gb'

@login_required
def import_hackingchinese_radicals(request):

	"""
		It would be much better to let this heavy work be done by a seperate process, one that is sufficiently
		detached to let Apache finish the request while the seperate process works. This would be much better
		for the user (now it loads a really long time) and performance (if a bunch of people upload files (more
		than Apache has worker processes) the server is unreachable until some are done. Implementing the better way
		would require not only a separate process (Celery?) but also some way to notify the user when done.
	""" #todo

	def parse(txt):
		data = []
		for line in txt.splitlines():
			if line:
				parts = line.split('\t')
				data.append((
					'{0} [radical]'.format(parts[0]),  # radical
					'{0}'.format(parts[4].strip(' ()')),  # pinyin
					'{0} [radical] e.g. {1} ; note: {2}'.format(parts[3], parts[5], parts[6]),  # definition
				))
		return data

	@transaction.atomic
	def make_list(data, learner, show_pinyin):
		if show_pinyin:
			li = TranslationsList(name = 'top 100 radicals (hackingchinese) show pinyin', public = True, language = CNY)
		else:
			li = TranslationsList(name = 'top 100 radicals (hackingchinese) hide pinyin', public = True, language = CNY)
		li.save()
		ListAccess(translations_list = li, learner = learner, access = ListAccess.EDIT).save()
		for radical, pinyin, definition in data:
			phrase = Phrase(learner = learner, public_edit = False)
			phrase.save()
			if show_pinyin:
				trans_cny = Translation(phrase = phrase, language = CNY, text = '%s %s' % (radical, pinyin))
				trans_en = Translation(phrase = phrase, language = EN, text = definition)
			else:
				trans_cny = Translation(phrase = phrase, language = CNY, text = '%s' % radical)
				trans_en = Translation(phrase = phrase, language = EN, text = '%s ; %s' % (pinyin, definition))
			trans_cny.save()
			trans_en.save()
			li.translations.add(trans_cny)
		return li

	form = ImportForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		parse(form.get_content())
		try:
			data = parse(form.get_content())
		except Exception:
			return notification(request, 'Sorry, there was a problem parsing this file.')
		""" Make the first list, which shows Pinyin """
		if not len(data):
			return notification(request, 'No data found')
		list_show_pinyin = make_list(data = data, learner = request.user, show_pinyin = True)
		list_hide_pinyin = make_list(data = data, learner = request.user, show_pinyin = False)
		return notification(request, 'Succesfully imported %d phrases! See the lists with <a href="%s">visible</a> and <a href="%s">hidden</a> pinyin.' % (
			list_show_pinyin.translations.count(),
			reverse('show_list', kwargs = {'pk': list_show_pinyin.pk}),
			reverse('show_list', kwargs = {'pk': list_hide_pinyin.pk}),
		))
	return render(request, 'import_form.html', {
		'message': 'Import the top 100 most common radicals from <a href="http://www.hackingchinese.com/kickstart-your-character-learning-with-the-100-most-common-radicals/">hackingchinese.com</a>.',
		'form': form,
	})


@login_required
def import_chinesepod_dialogue(request):
	#todo: make sure everything is imported privately
	form = ChinesepodForm(request.POST or None)
	if form.is_valid():
		opener = build_opener()
		opener.addheaders.append(('Cookie', '{0:s}={1:s}'.format(ChinesepodForm.COOKIE_NAME, form.cleaned_data['session'])))
		for url in form.cleaned_data['urls'].splitlines():
			if '#' in url:
				url = url.split('#')[0]
			url += '#dialogue-tab'
			html = opener.open(url).read()
	raise NotImplementedError('Not ready yet')
	return render(request, 'import_chinesepod.html', {
		'form': form,
	})


LANG_CODES = set(lang[0] for lang in settings.LANGUAGES)


@login_required
def import_structured_text(request, limit=100):
	#todo: search for duplicates
	form = TextForm(request.user)
	if form.is_valid():
		added_count = 0
		trans_li = form.cleaned_data['list']
		phrases = split(r'\s*\n\s*\n\s*', form.cleaned_data['text'])
		for phrasetxt in phrases:
			if not phrasetxt.strip():
				continue
			phrase = Phrase(learner=request.user, public_edit=form.cleaned_data['public_edit'])
			phrase.save()
			first = True
			translationtxts = phrasetxt.split('\n')
			for transtxt in translationtxts:
				try:
					langcode, txt = transtxt.split(None, maxsplit=1)
				except ValueError:
					return notification(request, 'like "{0:s}" seems not to consist of a langauge code + text'.format(
						transtxt))
				if not langcode in LANG_CODES:
					return notification(request, 'unknown language {0:s}; try one of {1:s}'.format(langcode,
						', '.join(LANG_CODES)))
				translation = Translation(phrase=phrase, langauge=langcode, text=txt)
				translation.save()
				added_count += 1
				if first:
					trans_li.translations.add(translation)
					first=False
				if added_count >= limit:
					return notification(request, ('Only {0:d} translations were added, the rest was skipped because '
						'the limit per submission was exceeded').format(added_count))
		return notification(request, 'All {0:d} translations added'.format(added_count))
	return render(request, 'import_structured_text.html', {
		'lang_codes': LANG_CODES,
		'form': LANG_CODES,
	})
