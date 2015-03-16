# -*- coding: utf-8 -*-

"""
	This is for database upgrades, you can ignore it and preferably don't change anything.
"""

from __future__ import unicode_literals
from django.db import migrations


def create_admin(apps, schema_editor):
	Learner = apps.get_model('learners', 'Learner')
	Translation = apps.get_model('phrasebook', 'Translation')
	TranslationsList = apps.get_model('lists', 'TranslationsList')
	ListAccess = apps.get_model('lists', 'ListAccess')
	admin = Learner.objects.filter(is_superuser = True)[0]
	li1 = TranslationsList(name = '42', public = True, language = None)
	li1.save()
	[li1.translations.add(trans) for trans in Translation.objects.all()]
	li2 = TranslationsList(name = 'Courtesy', public = False, language = 'zh-cn')
	li2.save()
	[li2.translations.add(trans) for trans in Translation.objects.filter(language = 'zh-cn')]
	li3 = TranslationsList(name = 'Courtesy', public = True, language = 'nl')
	li3.save()
	[li3.translations.add(trans) for trans in Translation.objects.filter(language = 'nl')]
	li4 = TranslationsList(name = 'unusable', public = True, language = None)
	li4.save()
	[li4.translations.add(trans) for trans in Translation.objects.filter(text = u'gezellig')]
	acc1 = ListAccess(translations_list = li1, learner = admin, access = 'edit', priority = 0, active = True)
	acc1.save()
	acc2 = ListAccess(translations_list = li2, learner = admin, access = 'view', priority = 10, active = False)
	acc2.save()
	#acc3 = ListAccess(translations_list = li3, learner = admin, access = 'edit', priority = 20, active = False)
	#acc3.save()
	acc4 = ListAccess(translations_list = li4, learner = admin, access = 'edit', priority = 60, active = True)
	acc4.save()


class Migration(migrations.Migration):

	dependencies = [
		('phrasebook', '0003_initital_phrases'),
		('lists', '0007_name_and_default'),
	]

	operations = [
		migrations.RunPython(create_admin)
	]


