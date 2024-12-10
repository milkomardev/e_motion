from django.contrib import messages
from django.shortcuts import redirect
from django.utils.timezone import now

from e_motion.accounts.models import Profile
from e_motion.schedule.models import Schedule


def fetch_training_and_profile(request, pk):
    training = Schedule.objects.get(pk=pk)
    profile = Profile.objects.get(user=request.user)

    return training, profile


def check_training_status(request, training):
    if training.has_passed():
        messages.error(request, "This class has already ended.")
        return redirect(request.META.get('HTTP_REFERER', 'schedule'))


def check_training_full(request, training):
    if training.is_full():
        messages.error(request, "This class is full. Join the waiting list instead.")
        return redirect(request.META.get('HTTP_REFERER', 'schedule'))


def check_subscription_expiry(profile, request):
    today = now().date()
    if profile.subscription_end_date and profile.subscription_end_date < today:
        profile.subscription_is_active = False
        profile.save()
        messages.error(
            request, "Your subscription has expired. You might consider renewing it."
        )


def check_attendance_limit(profile, request):
    if profile.attendance_count >= profile.subscription_plan.attendance_limit:
        profile.subscription_is_active = False
        profile.save()
        messages.error(
            request, "You have reached your attendance limit. Consider renewing your subscription."
        )


def update_attendance(profile, request, training):
    if profile.subscription_is_active:
        profile.attended_trainings.add(training)
        profile.attendance_count += 1
        profile.save()


def check_subscription_status(profile, request, training):
    if profile.subscription_plan:
        check_subscription_expiry(profile, request)
        check_attendance_limit(profile, request)
        update_attendance(profile, request, training)


def subscription_attendance_update(profile, request, training):

    if profile.subscription_plan and training in profile.attended_trainings.all():
        profile.attended_trainings.remove(training)
        profile.attendance_count -= 1

        # Reactivate subscription if attendance count is below the limit
        if (profile.attendance_count < profile.subscription_plan.attendance_limit and not profile.subscription_is_active
                and profile.subscription_end_date >= now().date()):
            profile.subscription_is_active = True
            messages.success(request, "You now have one more Training available until you reach the limit.")

        profile.save()