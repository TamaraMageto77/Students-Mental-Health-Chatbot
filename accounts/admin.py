from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserType

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'account_type', 'is_active', 'is_staff_display')
    list_filter = ('account_type', 'is_active', 'is_superuser')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    
    filter_horizontal = ('groups', 'user_permissions')  # Now these fields will exist

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {
            'fields': (
                'account_type',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'full_name',
                'account_type',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser'
            ),
        }),
    )

    def is_staff_display(self, obj):
        return obj.account_type == UserType.ADMINISTRATOR
    is_staff_display.short_description = 'Is Staff'
    is_staff_display.boolean = True