from datetime import timedelta
from django.test import TestCase
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from e_motion.schedule.models import Schedule
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ScheduleModelTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="testuser",
            password="password123",
            email="testuser@example.com",
        )

        self.schedule = Schedule.objects.create(
            training_title="Yoga Class",
            instructor_name="John Doe",
            date=now() + timedelta(days=1),
            duration=timedelta(hours=1),
            max_attendees=1,
        )

    def test_end_time_calculation(self):
        expected_end_time = self.schedule.date + self.schedule.duration
        self.assertEqual(self.schedule.end_time(), expected_end_time)

    def test_is_full(self):
        self.schedule.students.add(self.user)
        self.assertTrue(self.schedule.is_full())

    def test_has_passed(self):
        past_schedule = Schedule.objects.create(
            training_title="Past Yoga Class",
            instructor_name="Jane Smith",
            date=now() - timedelta(days=2),
            duration=timedelta(hours=1),
        )
        self.assertTrue(past_schedule.has_passed())

        future_schedule = Schedule.objects.create(
            training_title="Future Yoga Class",
            instructor_name="Jane Smith",
            date=now() + timedelta(days=2),
            duration=timedelta(hours=1),
        )
        self.assertFalse(future_schedule.has_passed())

    def test_can_cancel(self):
        schedule_cancellable = Schedule.objects.create(
            training_title="Cancellable Class",
            instructor_name="Alice",
            date=now() + timedelta(hours=4),
            duration=timedelta(hours=1),
        )
        schedule_non_cancellable = Schedule.objects.create(
            training_title="Non-Cancellable Class",
            instructor_name="Bob",
            date=now() + timedelta(hours=2),
            duration=timedelta(hours=1),
        )

        self.assertTrue(schedule_cancellable.can_cancel())
        self.assertFalse(schedule_non_cancellable.can_cancel())

    def test_clean_no_overlap(self):
        overlapping_schedule = Schedule(
            training_title="Overlapping Class",
            instructor_name="Charlie",
            date=self.schedule.date + timedelta(minutes=30),
            duration=timedelta(hours=1),
        )

        with self.assertRaises(ValidationError):
            overlapping_schedule.clean()

    def test_user_waiting_list_position(self):
        users = [
            UserModel.objects.create_user(
                username=f"user{i}",
                password="password123",
                email=f"user{i}@test.com",
                first_name=f"Test{i}",
                last_name=f"User{i}",
            ) for i in range(3)]
        for user in users:
            self.schedule.waiting_list.add(user)

        self.assertEqual(self.schedule.user_waiting_list_position(users[0]), 1)
        self.assertEqual(self.schedule.user_waiting_list_position(users[1]), 2)
        self.assertEqual(self.schedule.user_waiting_list_position(users[2]), 3)


