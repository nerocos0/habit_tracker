from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Habit, HabitLog


class HabitViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.habit = Habit.objects.create(user=self.user, title='Test Habit')

    def test_habit_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/habit/list.html')

    def test_habit_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(f'/habit/{self.habit.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/habit/detail.html')

    def test_habit_create_view(self):
        self.client.force_login(self.user)
        response = self.client.post('/habit/create/', {
            'title': 'New Habit',
            'description': '',
            'target': 1
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Habit.objects.filter(title='New Habit').exists())

    def test_habit_update_view(self):
        self.client.force_login(self.user)
        response = self.client.post(f'/habit/{self.habit.slug}/update/', {
            'title': 'Updated Habit',
            'description': '',
            'target': 1
        })
        self.assertEqual(response.status_code, 302)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.title, 'Updated Habit')

    def test_habit_delete_view(self):
        self.client.force_login(self.user)
        response = self.client.post(f'/habit/{self.habit.slug}/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())

    def test_habit_reverse_is_active_view(self):
        self.client.force_login(self.user)
        response = self.client.post(f'/habit/{self.habit.slug}/reverse/')
        self.assertEqual(response.status_code, 302)
        self.habit.refresh_from_db()
        self.assertFalse(self.habit.is_active)

    def test_habit_log_create_view(self):
        self.client.force_login(self.user)
        response = self.client.post(f'/habit/{self.habit.slug}/logs/create/', {
            'datetime': '12:00:00'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(HabitLog.objects.filter(habit=self.habit).exists())

    def test_habit_log_delete_view(self):
        self.client.force_login(self.user)
        log = HabitLog.objects.create(habit=self.habit, datetime='2026-10-1 12:00:00+03:00')
        response = self.client.post(f'/habit/{self.habit.slug}/logs/{log.id}/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(HabitLog.objects.filter(id=log.id).exists())

    def test_habit_detail_view_other_user(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.force_login(other_user)
        response = self.client.get(f'/habit/{self.habit.slug}/')
        self.assertEqual(response.status_code, 404)