
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from phrasebook.models import Phrase, Translation


"""
	This puts the models in yoursite.com/admin/ where you as owner can edit it directly.
"""
class PhraseAdmin(ModelAdmin):
	list_display = ('__str__', 'learner', 'public_edit',)

admin.site.register(Phrase, PhraseAdmin)

class TranslationAdmin(ModelAdmin):
	list_display = ('__str__', 'language', 'phrase')

admin.site.register(Translation, TranslationAdmin)


