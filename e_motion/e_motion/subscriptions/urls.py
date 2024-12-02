from django.urls import path

from e_motion.subscriptions import views

urlpatterns = [
    path('', views.PricingView.as_view(), name='pricing'),
]