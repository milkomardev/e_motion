from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('e_motion.common.urls')),
    path('accounts/', include('e_motion.accounts.urls')),
    path('trainings/', include('e_motion.trainings.urls')),
    path('schedule/', include('e_motion.schedule.urls')),
]
