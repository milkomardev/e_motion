from datetime import timedelta

from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.timezone import now
from django.views.generic import TemplateView

from .models import Schedule


class ScheduleView(TemplateView):
    template_name = 'schedule/schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())

        trainings = Schedule.objects.filter(date__date__gte=start_of_week).order_by('date')
        schedule = {}

        for training in trainings:
            training_date = training.date.date()

            if training_date not in schedule:
                schedule[training_date] = {
                    'date': training_date,
                    'day_name': training.date.strftime('%A'),
                    'trainings': [],
                }

            waiting_list_position = None

            if self.request.user in training.waiting_list.all():
                waiting_list_position = list(training.waiting_list.all()).index(self.request.user) + 1

            schedule[training_date]['trainings'].append({
                'training': training,
                'waiting_list_position': waiting_list_position,
            })

        context['schedule'] = schedule
        return context


def make_reservation(request, pk):
    training = get_object_or_404(Schedule, pk=pk)
    if training.is_full():
        messages.error(request, "The class is full. Join the waiting list instead.")
        return redirect('schedule')
    training.students.add(request.user)
    messages.success(request, "Reservation successful!")
    return redirect('schedule')


def cancel_reservation(request, pk):
    training = get_object_or_404(Schedule, pk=pk)
    training.students.remove(request.user)

    if training.waiting_list.exists():
        next_user = training.waiting_list.first()
        training.waiting_list.remove(next_user)
        training.students.add(next_user)

    messages.success(request, "Reservation canceled.")
    return redirect('schedule')


def join_waiting_list(request, pk):
    training = get_object_or_404(Schedule, pk=pk)
    if request.user in training.students.all():
        messages.error(request, "You are already enrolled in the class.")
        return redirect('schedule')
    training.waiting_list.add(request.user)
    messages.success(request, "Added to the waiting list.")
    return redirect('schedule')


def withdraw_waiting_list(request, pk):
    training = get_object_or_404(Schedule, pk=pk)
    if request.user in training.waiting_list.all():
        training.waiting_list.remove(request.user)
        messages.success(request, "You have been removed from the waiting list.")
    else:
        messages.error(request, "You are not on the waiting list for this class.")
    return redirect('schedule')

