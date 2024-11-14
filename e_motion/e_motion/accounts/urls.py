from django.urls import path, include

from e_motion.accounts import views

urlpatterns = [
    path('', views.home, name='home'),
]


