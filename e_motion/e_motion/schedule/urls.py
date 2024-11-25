from django.urls import path, include

from e_motion.schedule import views

urlpatterns = [
    path('', views.ScheduleView.as_view(), name='schedule'),
    path('create/', views.ScheduleCreateView.as_view(), name='schedule-create'),
    path('<int:pk>/', include([
        path('reserve/', views.make_reservation, name='make-reservation'),
        path('cancel/', views.cancel_reservation, name='cancel-reservation'),
        path('join-waiting-list/', views.join_waiting_list, name='join-waiting-list'),
        path('withdraw-waiting-list/', views.withdraw_waiting_list, name='withdraw-waiting-list'),
        path('edit/', views.ScheduleUpdateView.as_view(), name='schedule-edit'),
        path('delete/', views.ScheduleDeleteView.as_view(), name='schedule-delete'),
    ])),
]
