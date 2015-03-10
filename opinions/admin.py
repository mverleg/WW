
from django.contrib import admin
from opinions.models import TranslationVote, TranslationComment


class TranslationVoteAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'translation', 'learner', 'up',)


class TranslationCommentAdmin(admin.ModelAdmin):
	readonly_fields = ('added', 'edited',)
	list_display = ('__unicode__', 'translation', 'learner', 'edited',)


admin.site.register(TranslationVote, TranslationVoteAdmin)
admin.site.register(TranslationComment, TranslationCommentAdmin)


