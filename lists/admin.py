
from django.contrib import admin
from lists.models import PhraseList, ListAccess


class ListAccessAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'phrase_list', 'learner', 'active', 'access', 'priority',)


class PhraseListAdmin(admin.ModelAdmin):
	list_display = ('__unicode__',)



admin.site.register(PhraseList, PhraseListAdmin)
admin.site.register(ListAccess, ListAccessAdmin)


