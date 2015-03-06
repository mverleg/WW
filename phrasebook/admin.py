
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from phrasebook.models import Phrase, Translation


"""
	This puts the models in yoursite.com/admin/ where you as owner can edit it directly. You can customize this a lot
	but the default is often already useful.
"""
admin.site.register(Phrase)

class TranslationAdmin(ModelAdmin):
	list_display = ('__unicode__', 'language', 'phrase')

admin.site.register(Translation, TranslationAdmin)


