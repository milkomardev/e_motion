from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils.timezone import now, make_aware
from datetime import timedelta, datetime

from django.contrib.auth import get_user_model

from e_motion.schedule.models import Schedule
from e_motion.schedule.views import ScheduleView

UserModel = get_user_model()


class ScheduleViewTests(TestCase):
    def setUp(self):

        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(
            username="testuser",
            password="Password12@#",
            email="test@test.com",
            first_name="Test",
            last_name="User"
        )

        self.client.login(username="testuser", password="Password12@#")

        today = now().date()
        self.start_of_week = today - timedelta(days=today.weekday())

        for i in range(5):
            Schedule.objects.create(
                date=make_aware(datetime.combine(self.start_of_week + timedelta(days=i), datetime.min.time())),
                duration=timedelta(hours=1),
            )

        for i in range(2):
            Schedule.objects.create(
                date=make_aware(datetime.combine(self.start_of_week + timedelta(weeks=1, days=i), datetime.min.time())),
                duration=timedelta(hours=1),
            )

    def test_schedule_view_renders_correct_template(self):
        request = self.factory.get(reverse("schedule"))
        request.user = self.user
        response = ScheduleView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("schedule/schedule.html", response.template_name)

    def test_schedule_view_current_week_context(self):
        request = self.factory.get(reverse("schedule"))
        request.user = self.user
        response = ScheduleView.as_view()(request)
        context = response.context_data

        week_start = self.start_of_week
        week_end = week_start + timedelta(days=6)

        self.assertEqual(context["week_start"], week_start)
        self.assertEqual(context["week_end"], week_end)
        self.assertIn("week_range", context)
        self.assertIn("has_next_week", context)
        self.assertIn("has_previous_week", context)

    def test_schedule_view_next_week_context(self):
        request = self.factory.get(reverse("schedule") + "?week=1")
        request.user = self.user
        response = ScheduleView.as_view()(request)
        context = response.context_data

        week_start = self.start_of_week + timedelta(weeks=1)
        week_end = week_start + timedelta(days=6)

        self.assertEqual(context["week_start"], week_start)
        self.assertEqual(context["week_end"], week_end)
        self.assertTrue(context["has_previous_week"])

    def test_schedule_view_has_next_week(self):
        request = self.factory.get(reverse("schedule") + "?week=0")
        request.user = self.user
        response = ScheduleView.as_view()(request)
        context = response.context_data

        self.assertTrue(context["has_next_week"])

    def test_schedule_view_has_previous_week(self):
        request = self.factory.get(reverse("schedule") + "?week=1")
        request.user = self.user
        response = ScheduleView.as_view()(request)
        context = response.context_data

        self.assertTrue(context["has_previous_week"])
