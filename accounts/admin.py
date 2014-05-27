from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from guardian.admin import GuardedModelAdmin

class DSUserAdmin(UserAdmin):
    pass
    
admin.site.unregister(User)
admin.site.register(User, DSUserAdmin)

admin.site.unregister(Group)
admin.site.register(Group, GuardedModelAdmin)
