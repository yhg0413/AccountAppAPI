from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from users.models import User


# Create your tests here.


class RegisterViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_register_user(self):
        client = APIClient()
        data = {
            "email": 'test@test.com',
            "password": "@TEST1234"
        }
        response = client.post('/users/signup', data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['email'], 'test@test.com')


class AuthViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="test2@test.com", password="@TEST1234")

    def test_view_login(self):
        client = APIClient()
        data = {
            "email": 'test2@test.com',
            "password": "@TEST1234"
        }
        response = client.post('/users/auth', data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(list(response.json()['results'].keys())[0], 'access_token')
        self.assertEquals(list(response.json()['results'].keys())[1], 'refresh_token')

    def test_view_logout(self):
        client = APIClient()
        data = {
            "email": 'test2@test.com',
            "password": "@TEST1234"
        }
        response = client.post('/users/auth', data)
        self.assertEquals(response.status_code, 200)

        response = client.get('/users/auth')
        self.assertEquals(bool(client.cookies['jwt'].value), False)
        self.assertEquals(bool(client.cookies['jwt_r'].value), False)
