from django.urls import path, include
from e_motion.instructors import views

urlpatterns = [
    path('', views.InstructorListView.as_view(), name='instructors-list'),
    path('create/', views.InstructorCreateView.as_view(), name='instructor-create'),
    path('<int:pk>/', include([
        path('details/', views.InstructorDetailView.as_view(), name='instructor-details'),
        path('edit/', views.InstructorUpdateView.as_view(), name='instructor-edit'),
        path('delete/', views.InstructorDeleteView.as_view(), name='instructor-delete'),
    ])),
]
