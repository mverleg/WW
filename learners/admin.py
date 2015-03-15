
from django.contrib import admin
from django.contrib.auth.models import Group
from learners.models import Learner


class LearnerAdmin(admin.ModelAdmin):
	exclude = ('groups',)
	fields = ('name', 'email', 'is_staff', 'is_superuser', 'user_permissions', 'last_login', 'password',
		'add_randomness', 'minimum_delay', 'new_count', 'show_medium_correctness', 'phrase_index', 'need_active_update',)
	readonly_fields = ('last_login', 'password',)
	list_display = ('name', 'email', 'is_staff', 'is_superuser', 'last_login', 'phrase_index',)


admin.site.register(Learner, LearnerAdmin)
admin.site.unregister(Group)


