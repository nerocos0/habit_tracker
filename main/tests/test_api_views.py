from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.utils import timezone

from ..models import Habit

class HabitViewsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.habit = Habit.objects.create(user=self.user, title='Test Habit')
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
 

    def test_habit_list_api(self):
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 1)

    def test_habit_detail_api(self):
        response = self.client.get(f'/api/habits/{self.habit.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Habit')

    def test_habit_create_api(self):
        response = self.client.post('/api/habits/', {
            'title': 'New Habit',
            'description': '',
            'target': 1
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Habit.objects.filter(title='New Habit').exists())

    def test_habit_update_api(self):
        response = self.client.patch(f'/api/habits/{self.habit.slug}/', {
            'title': 'Updated Habit'
        })
        self.assertEqual(response.status_code, 200)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.title, 'Updated Habit')

    def test_habit_delete_api(self):
        response = self.client.delete(f'/api/habits/{self.habit.slug}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())

    def test_habit_reverse_is_active_api(self):
        response = self.client.post(f'/api/habits/{self.habit.slug}/reverse_active/')
        self.assertEqual(response.status_code, 200)
        self.habit.refresh_from_db()
        self.assertFalse(self.habit.is_active)

    def test_habit_log_create_api(self):
        response = self.client.post(f'/api/habits/{self.habit.slug}/logs/', {
            'time_input': '12:00'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.habit.habit_logs.exists())

        log = self.habit.habit_logs.first()
        local_dt = timezone.localtime(log.datetime)
        self.assertEqual(local_dt.hour, 12)
        self.assertEqual(local_dt.minute, 0)

    def test_habit_log_delete_api(self):
        habit_log = self.habit.habit_logs.create(datetime='2025-01-01 12:00:00+03:00')
        response = self.client.delete(f'/api/habits/{self.habit.slug}/logs/{habit_log.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(self.habit.habit_logs.filter(id=habit_log.id).exists())

    def test_habit_list_api_unauthenticated(self):
        self.client.credentials()  # Убираем токен авторизации
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, 401)

    def test_habit_detail_another_user_api(self):
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
        another_habit = Habit.objects.create(user=another_user, title='Another Habit')
        response = self.client.get(f'/api/habits/{another_habit.slug}/')
        self.assertEqual(response.status_code, 404)