from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.timezone import now
from datetime import timedelta

from .forms import ScheduleCreateForm, ScheduleUpdateForm
from .models import Schedule
from .utils import fetch_training_and_profile, check_training_status, check_training_full, check_subscription_status, \
    subscription_attendance_update, check_for_next_user_in_waiting_list
from ..accounts.models import Profile


class ScheduleView(ListView):
    model = Schedule
    template_name = 'schedule/schedule.html'
    context_object_name = 'schedule'

    def get_week_dates(self):
        today = now().date()
        start_of_current_week = today - timedelta(days=today.weekday())
        week_offset = int(self.request.GET.get('week', 0))
        week_start = start_of_current_week + timedelta(weeks=week_offset)

        if week_start < start_of_current_week:
            week_start = start_of_current_week

        week_end = week_start + timedelta(days=6)
        return week_start, week_end

    def get_queryset(self):
        week_start, week_end = self.get_week_dates()
        return Schedule.objects.filter(date__date__gte=week_start, date__date__lte=week_end).order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        week_start, week_end = self.get_week_dates()
        week_offset = int(self.request.GET.get('week', 0))

        week_range = f"{week_start.strftime('%d.%m')} - {week_end.strftime('%d.%m')}"
        has_next_week = Schedule.objects.filter(date__date__gt=week_end).exists()
        has_previous_week = week_offset > 0

        trainings = Schedule.objects.filter(date__date__gte=week_start, date__date__lte=week_end).order_by('date')

        schedule = {}
        for training in trainings:
            training_date = training.date.date()
            if training_date not in schedule:
                schedule[training_date] = {
                    'day_name': training.date.strftime('%A'),
                    'date': training_date,
                    'trainings': [],
                }
            schedule[training_date]['trainings'].append(training)

        context['schedule'] = schedule
        context['has_next_week'] = has_next_week
        context['has_previous_week'] = has_previous_week
        context['week_range'] = week_range
        context['week_start'] = week_start
        context['week_end'] = week_end
        context['week_offset'] = week_offset
        return context


class ScheduleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Schedule
    form_class = ScheduleCreateForm
    template_name = 'schedule/schedule-create.html'
    success_url = reverse_lazy('schedule')

    def test_func(self):
        return self.request.user.has_perm("schedule.add_schedule")


class ScheduleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Schedule
    form_class = ScheduleUpdateForm
    template_name = 'schedule/schedule-edit.html'
    success_url = reverse_lazy('schedule')

    def test_func(self):
        return self.request.user.has_perm("schedule.change_schedule")


class ScheduleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Schedule
    template_name = 'schedule/schedule-delete.html'
    success_url = reverse_lazy('schedule')

    def test_func(self):
        return self.request.user.has_perm("schedule.delete_schedule")


@login_required
async def make_reservation(request, pk):
    training, profile = await sync_to_async(fetch_training_and_profile)(request, pk)

    await sync_to_async(check_training_status)(request, training)
    await sync_to_async(check_training_full)(request, training)
    await sync_to_async(check_subscription_status)(profile, request, training)

    await sync_to_async(training.students.add)(request.user)
    await sync_to_async(messages.success)(request, "Reservation successful!")
    return redirect(request.META.get('HTTP_REFERER', 'schedule'))




@login_required
async def cancel_reservation(request, pk):
    training, profile = await sync_to_async(fetch_training_and_profile)(request, pk)

    await sync_to_async(training.students.remove)(request.user)
    await sync_to_async(subscription_attendance_update)(profile, request, training)

    await sync_to_async(messages.success)(request, "Reservation cancelled.")
    await sync_to_async(check_for_next_user_in_waiting_list)(training)
    return redirect(request.META.get('HTTP_REFERER', 'schedule'))


@login_required
def join_waiting_list(request, pk):
    training = get_object_or_404(Schedule, pk=pk)
    if request.user in training.students.all():
        messages.error(request, "You are already enrolled in the class.")
        return redirect('schedule')
    training.waiting_list.add(request.user)
    messages.success(request, "Added to the waiting list.")
    return redirect(request.META.get('HTTP_REFERER', 'schedule'))


@login_required
def withdraw_waiting_list(request, pk):
    training = get_object_or_404(Schedule, pk=pk)
    if request.user in training.waiting_list.all():
        training.waiting_list.remove(request.user)
        messages.success(request, "You have been removed from the waiting list.")
    else:
        messages.error(request, "You are not on the waiting list for this class.")
    return redirect(request.META.get('HTTP_REFERER', 'schedule'))
