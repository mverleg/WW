
from django.contrib import admin
from lists.models import TranslationsList, ListAccess


class ListAccessAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'translations_list', 'learner', 'active', 'access', 'priority',)


class TranslationListAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'language',)



admin.site.register(TranslationsList, TranslationListAdmin)
admin.site.register(ListAccess, ListAccessAdmin)


