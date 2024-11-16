from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from e_motion.accounts import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', include([
        path('', views.ProfileDetailsView.as_view(), name='profile-details'),
        path('edit/', views.ProfileEditView.as_view(), name='profile-edit'),
        path('delete/', views.ProfileDeleteView.as_view(), name='profile-delete'),
    ]))
]