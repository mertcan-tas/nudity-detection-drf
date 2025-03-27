from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from account.models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name','surname')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'is_active', 'is_staff'),
        }),
    )

    list_display = ('email', 'name', 'is_active', 'is_staff')
    search_fields = ('email', 'name',)
    ordering = ('email',)
    readonly_fields = ('created_at', 'updated_at')
    
admin.site.register(User, UserAdmin)