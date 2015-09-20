# -*- coding: utf-8 -*-

"""
	This is for database upgrades, you can ignore it and preferably don't change anything.
"""

from django.db import migrations


def create_admin(apps, schema_editor):
	Learner = apps.get_model('learners', 'Learner')
	Phrase = apps.get_model('phrasebook', 'Phrase')
	Translation = apps.get_model('phrasebook', 'Translation')
	admin = Learner.objects.filter(is_superuser = True)[0]
	phrase1 = Phrase(learner = admin, public_edit = True)
	phrase1.save()
	transs = [
		Translation(phrase = phrase1, language = 'en-gb', text = 'good day'),
		Translation(phrase = phrase1, language = 'zh-cn', text = '你好'),
		Translation(phrase = phrase1, language = 'de', text = 'guten Tag'),
		Translation(phrase = phrase1, language = 'nl', text = 'goedendag'),
	]
	[trans.save() for trans in transs]
	phrase2 = Phrase(learner = None, public_edit = False)
	phrase2.save()
	transs = [
		Translation(phrase = phrase2, language = 'en-gb', text = 'thanks'),
		Translation(phrase = phrase2, language = 'zh-cn', text = '谢谢'),
		Translation(phrase = phrase2, language = 'de', text = 'danke'),
		Translation(phrase = phrase2, language = 'nl', text = 'dank u'),
	]
	[trans.save() for trans in transs]
	phrase3 = Phrase(learner = admin, public_edit = True)
	phrase3.save()
	transs = [
		Translation(phrase = phrase3, language = 'zh-cn', text = '晚安'),
		Translation(phrase = phrase3, language = 'nl', text = 'slaap lekker'),
	]
	[trans.save() for trans in transs]
	phrase4 = Phrase(learner = admin, public_edit = True)
	phrase4.save()
	transs = [
		Translation(phrase = phrase4, language = 'nl', text = 'gezellig'),
	]
	[trans.save() for trans in transs]
	phrase5 = Phrase(learner = admin, public_edit = False)
	phrase5.save()
	transs = [
		Translation(phrase = phrase5, language = 'zh-cn', text = '美丽'),
		Translation(phrase = phrase5, language = 'de', text = 'schön'),
		Translation(phrase = phrase5, language = 'nl', text = 'mooi'),
	]
	[trans.save() for trans in transs]


class Migration(migrations.Migration):

	dependencies = [
		('learners', '0013_favor_unknown'),
		('phrasebook', '0002_new_access'),
		('lists', '0007_name_and_default'),
	]

	operations = [
		migrations.RunPython(create_admin)
	]


