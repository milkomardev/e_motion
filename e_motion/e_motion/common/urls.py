from django.urls import path
from e_motion.common import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.contact_detail, name='contacts'),
]
