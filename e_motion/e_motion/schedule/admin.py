from django.contrib import admin

from e_motion.schedule.models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('training', 'date', 'duration', 'max_attendees', 'display_instructors')
    list_filter = ('training__title', 'date', 'training__instructor__user__username')
    search_fields = ('training__title', 'training__instructor__user__first_name', 'training__instructor__user__last_name')
    date_hierarchy = 'date'

    def display_instructors(self, obj):
        return obj.training.instructor.user.get_full_name()
    display_instructors.short_description = 'Instructor'

