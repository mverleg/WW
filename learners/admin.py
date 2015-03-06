
from django.contrib import admin
from django.contrib.auth.models import Group
from learners.models import Learner


admin.site.register(Learner)
admin.site.unregister(Group)


