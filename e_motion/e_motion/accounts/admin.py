from datetime import timedelta

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
        'subscription_is_active',
        'attendance_count',
        'subscription_start_date',
        'subscription_end_date',
        'profile_picture',
    )

    readonly_fields = ('attendance_count',)

    def save_model(self, request, obj, form, change):
        if obj.subscription_plan and obj.subscription_start_date:
            duration = timedelta(days=30 * obj.subscription_plan.duration_months)
            obj.subscription_end_date = obj.subscription_start_date + duration
            obj.attendance_count = 0
        super().save_model(request, obj, form, change)


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
