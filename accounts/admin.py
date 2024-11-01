from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomAdmin(UserAdmin):
    model = CustomUser
    list_display = ( 'email', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'email', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                )
            }
        ),
    )
    search_fields = ('email', 'date_joined')
    ordering = ('email',)


admin.site.register(CustomUser, CustomAdmin)