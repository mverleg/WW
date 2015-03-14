
from django.contrib import admin
from study.models import Result


class ResultAdmin(admin.ModelAdmin):
	list_display = ('get_result_display', 'learner', 'translation', 'language',)


admin.site.register(Result, ResultAdmin)


