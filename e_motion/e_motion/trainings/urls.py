from django.urls import path, include

from e_motion.trainings import views

urlpatterns = [
    path('', views.TrainingListView.as_view(), name='trainings-list'),
    path('<int:pk>/', include([
        path('details/', views.TrainingDetailView.as_view(), name='training-details'),
    ])),
]
