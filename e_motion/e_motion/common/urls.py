from django.urls import path
from e_motion.common import views
from e_motion.common.views import ContactDetailView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', ContactDetailView.as_view(), name='contacts'),
]
