from django.contrib import admin

from e_motion.instructors.models import Instructor


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user__username', 'user__first_name', 'user__last_name', 'bio']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']