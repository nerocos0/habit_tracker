from django.test import TestCase
from unidecode import unidecode
from django.utils.text import slugify
from django.db import IntegrityError
from django.utils import timezone

from django.contrib.auth.models import User
from ..models import Habit, HabitLog

class HabitModelTestCase(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.habit = Habit.objects.create(
            user=self.user,
            title='Зарядка',
        )

    def test_habit_str(self):
        self.assertEqual(str(self.habit), 'Зарядка')

    def test_habit_slug_generated_and_transliterated(self):
        slug = self.habit.slug
        transliterated_title = unidecode(self.habit.title)
        self.assertIsNotNone(slug)
        self.assertEqual(slug, f'{slugify(transliterated_title)}-{self.habit.user_id}')

    def test_unique_slug(self):
        user2=User.objects.create_user(
            username='testuser2',
            password='testpassword2'
        )

        habit2 = Habit.objects.create(
            user=user2,
            title='Зарядка',
        )
        self.assertEqual(self.habit.title, habit2.title)
        self.assertIn(str(user2.id), habit2.slug)
        self.assertIn(str(self.user.id), self.habit.slug)
        self.assertNotEqual(self.habit.slug, habit2.slug)

    def test_unique_user_habit(self):
        with self.assertRaises(IntegrityError):
            Habit.objects.create(
                user=self.user,
                title='Зарядка'
            )

    def test_habit_log_str(self):
        datetime='2026-10-1 12:00:00+03:00'
        log = HabitLog.objects.create(
            habit=self.habit,
            datetime=datetime
        )
        self.assertEqual(str(log), f'{self.habit.title} - {datetime}')

    def test_habit_log_ordering(self):
        log_older = HabitLog.objects.create(
            habit=self.habit,
            datetime='2025-01-01 00:00:00+03:00'
        )
        log_new = HabitLog.objects.create(
            habit=self.habit,
            datetime='2026-10-01 12:00:00+03:00'
        )
        self.assertListEqual(list(self.habit.habit_logs.all()), [log_new, log_older])