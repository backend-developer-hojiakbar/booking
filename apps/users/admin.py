from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import User, PhoneToken


@admin.register(User)
class UserAdmin(UserAdmin):
    ordering = ('-id',)
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'is_active')

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
        ('Extra info', {'fields': ('rating', 'rapidlyReply', 'description', 'image', 'role')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )

    search_fields = ('phone_number', 'first_name', 'last_name')

    list_filter = ('is_staff', 'is_active')


@admin.register(PhoneToken)
class PhoneTokenAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'token', 'created_at', 'expires_at', 'is_verified')

    search_fields = ('phone_number', 'token')