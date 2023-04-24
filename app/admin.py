from django.contrib import admin
from .models import Profile, Task, Goal, Quota
# Register your models here.
admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Goal)
admin.site.register(Quota)