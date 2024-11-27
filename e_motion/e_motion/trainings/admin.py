from django.contrib import admin

from e_motion.trainings.models import Training


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', ]
    search_fields = ['title', 'instructor__name']