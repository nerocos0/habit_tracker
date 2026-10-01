from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class AuthAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_obtain_token(self):
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'})
        refresh_token = response.data['refresh']
        response = self.client.post('/api/token/refresh/', {'refresh': refresh_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_invalid_credentials(self):
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 401)

    def test_invalid_refresh_token(self):
        response = self.client.post('/api/token/refresh/', {'refresh': 'invalidtoken'})
        self.assertEqual(response.status_code, 401)

    def test_access_protected_endpoint(self):
        # Получаем токен
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'})
        access_token = response.data['access']

        # Доступ к защищенному эндпоинту с токеном
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, 200)

        # Доступ к защищенному эндпоинту без токена
        self.client.credentials()  # Убираем токен авторизации
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, 401)