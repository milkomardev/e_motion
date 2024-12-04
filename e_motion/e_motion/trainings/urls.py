from django.urls import path, include
from e_motion.trainings import views

urlpatterns = [
    path('', views.TrainingListView.as_view(), name='trainings-list'),
    path('create/', views.TrainingCreateView.as_view(), name='training-create'),
    path('<slug:slug>/', include([
        path('details/', views.TrainingDetailView.as_view(), name='training-details'),
        path('edit/', views.TrainingEditView.as_view(), name='training-edit'),
        path('delete/', views.TrainingDeleteView.as_view(), name='training-delete'),
    ])),
]
