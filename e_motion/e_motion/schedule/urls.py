from django.urls import path, include

from e_motion.schedule import views

urlpatterns = [
    path('', views.ScheduleView.as_view(), name='schedule'),
    path('<int:pk>/', include([
        path('reserve/', views.make_reservation, name='make_reservation'),
        path('cancel/', views.cancel_reservation, name='cancel_reservation'),
        path('join-waiting-list/', views.join_waiting_list, name='join_waiting_list'),
        path('withdraw-waiting-list/', views.withdraw_waiting_list, name='withdraw_waiting_list'),
    ])),
]