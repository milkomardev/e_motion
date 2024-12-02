from django.urls import path, include
from e_motion.common import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.contact_detail, name='contacts'),
    path('gallery/', include([
        path('', views.GalleryListView.as_view(), name='gallery-list'),
        path('add/', views.GalleryCreateView.as_view(), name='gallery-add'),
        path('delete/<int:pk>/', views.GalleryDeleteView.as_view(), name='gallery-delete'),
    ])),
]
