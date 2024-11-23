from datetime import timedelta

from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.timezone import now
from django.views.generic import TemplateView

from .models import Schedule

from django.views.generic import ListView
from django.utils.timezone import now
from datetime import timedelta
from .models import Schedule


class ScheduleView(ListView):
    model = Schedule
    template_name = 'schedule/schedule.html'
    context_object_name = 'schedule'
    paginate_by = 7  # Show one week (7 days) per page

    def get_queryset(self):
        # Get today's date and the start of the current week
        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week

        # Get the week offset from the query parameter
        week_offset = int(self.request.GET.get('week', 0))  # Default to 0 (current week)
        week_start = start_of_week + timedelta(weeks=week_offset)
        week_end = week_start + timedelta(days=6)

        # Filter trainings for the current week
        return Schedule.objects.filter(date__date__gte=week_start, date__date__lte=week_end).order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate week range for display
        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())
        week_offset = int(self.request.GET.get('week', 0))
        week_start = start_of_week + timedelta(weeks=week_offset)
        week_end = week_start + timedelta(days=6)
        week_range = f"{week_start.strftime('%d.%m')} - {week_end.strftime('%d.%m')}"

        has_next_week = Schedule.objects.filter(date__date__gt=week_end).exists()
        has_previous_week = Schedule.objects.filter(date__date__lt=week_start).exists()

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
        context['week_offset'] = week_offset  # Pass the current week offset for navigation
        return context


# class ScheduleView(TemplateView):
#     template_name = 'schedule/schedule.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         today = now().date()
#         start_of_week = today - timedelta(days=today.weekday())
#
#         trainings = Schedule.objects.filter(date__date__gte=start_of_week).order_by('date')
#         schedule = {}
#
#         for training in trainings:
#             training_date = training.date.date()
#
#             if training_date not in schedule:
#                 schedule[training_date] = {
#                     'date': training_date,
#                     'day_name': training.date.strftime('%A'),
#                     'trainings': [],
#                 }
#
#             waiting_list_position = None
#
#             if self.request.user in training.waiting_list.all():
#                 waiting_list_position = list(training.waiting_list.all()).index(self.request.user) + 1
#
#             schedule[training_date]['trainings'].append({
#                 'training': training,
#                 'waiting_list_position': waiting_list_position,
#             })
#
#         context['schedule'] = schedule
#         return context


def make_reservation(request, pk):
    training = get_object_or_404(Schedule, pk=pk)

    if training.has_passed():
        messages.error(request, "This class has already ended.")
    elif training.is_full():
        messages.error(request, "This class is full. Join the waiting list instead.")
    else:
        training.students.add(request.user)
        messages.success(request, "Reservation successful!")

    # Redirect back to the referring page or default to the schedule page
    return redirect(request.META.get('HTTP_REFERER', 'schedule'))


def cancel_reservation(request, pk):
    training = get_object_or_404(Schedule, pk=pk)
    training.students.remove(request.user)

    if training.waiting_list.exists():
        next_user = training.waiting_list.first()
        training.waiting_list.remove(next_user)
        training.students.add(next_user)

    messages.success(request, "Reservation canceled.")
    return redirect(request.META.get('HTTP_REFERER', 'schedule'))


def join_waiting_list(request, pk):
    training = get_object_or_404(Schedule, pk=pk)
    if request.user in training.students.all():
        messages.error(request, "You are already enrolled in the class.")
        return redirect('schedule')
    training.waiting_list.add(request.user)
    messages.success(request, "Added to the waiting list.")
    return redirect(request.META.get('HTTP_REFERER', 'schedule'))


def withdraw_waiting_list(request, pk):
    training = get_object_or_404(Schedule, pk=pk)
    if request.user in training.waiting_list.all():
        training.waiting_list.remove(request.user)
        messages.success(request, "You have been removed from the waiting list.")
    else:
        messages.error(request, "You are not on the waiting list for this class.")
    return redirect(request.META.get('HTTP_REFERER', 'schedule'))

