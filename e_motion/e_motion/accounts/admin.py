from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from e_motion.accounts.forms import AppUserChangeForm, AppUserCreationForm
from e_motion.accounts.models import Profile

UserModel = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fields = (
        'phone_number',
        'date_of_birth',
        'subscription_plan',
        'attendance_limit',
        'subscription_start_date',
        'subscription_end_date',
        'subscription_active',
        'profile_picture',
    )


@admin.register(UserModel)
class UserModelAdmin(UserAdmin):
    inlines = (ProfileInline,)
    form = AppUserChangeForm
    add_form = AppUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'username')
    search_fields = ('email', 'first_name', 'last_name', 'username')

    fieldsets = (
        ('Credentials', {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            'User Information',
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )