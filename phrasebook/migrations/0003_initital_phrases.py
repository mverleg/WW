# -*- coding: utf-8 -*-

"""
	This is for database upgrades, you can ignore it and preferably don't change anything.
"""

from __future__ import unicode_literals
from django.db import migrations


def create_admin(apps, schema_editor):
	Learner = apps.get_model('learners', 'Learner')
	Phrase = apps.get_model('phrasebook', 'Phrase')
	Translation = apps.get_model('phrasebook', 'Translation')
	admin = Learner.objects.filter(is_superuser = True)[0]
	phrase1 = Phrase(learner = admin, public_edit = True)
	phrase1.save()
	transs = [
		Translation(phrase = phrase1, language = 'en-gb', text = u'good day'),
		Translation(phrase = phrase1, language = 'zh-cn', text = u'你好'),
		Translation(phrase = phrase1, language = 'de', text = u'guten Tag'),
		Translation(phrase = phrase1, language = 'nl', text = u'goedendag'),
	]
	[trans.save() for trans in transs]
	phrase2 = Phrase(learner = None, public_edit = False)
	phrase2.save()
	transs = [
		Translation(phrase = phrase2, language = 'en-gb', text = u'thanks'),
		Translation(phrase = phrase2, language = 'zh-cn', text = u'谢谢'),
		Translation(phrase = phrase2, language = 'de', text = u'danke'),
		Translation(phrase = phrase2, language = 'nl', text = u'dank u'),
	]
	[trans.save() for trans in transs]
	phrase3 = Phrase(learner = admin, public_edit = True)
	phrase3.save()
	transs = [
		Translation(phrase = phrase3, language = 'zh-cn', text = u'晚安'),
		Translation(phrase = phrase3, language = 'nl', text = u'slaap lekker'),
	]
	[trans.save() for trans in transs]
	phrase4 = Phrase(learner = admin, public_edit = True)
	phrase4.save()
	transs = [
		Translation(phrase = phrase4, language = 'nl', text = u'gezellig'),
	]
	[trans.save() for trans in transs]
	phrase5 = Phrase(learner = admin, public_edit = False)
	phrase5.save()
	transs = [
		Translation(phrase = phrase5, language = 'zh-cn', text = u'美丽'),
		Translation(phrase = phrase5, language = 'de', text = u'schön'),
		Translation(phrase = phrase5, language = 'nl', text = u'mooi'),
	]
	[trans.save() for trans in transs]


class Migration(migrations.Migration):

	dependencies = [
		('learners', '0012_study_active_instead'),
		('phrasebook', '0002_new_access'),
		('lists', '0007_name_and_default'),
	]

	operations = [
		migrations.RunPython(create_admin)
	]


