from django.test import TestCase
from rest_framework.test import APITestCase, APIClient

from article.models import ArticleModels
from users.models import User


# Create your tests here.


class ArticleAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="test2@test.com", password="@TEST1234")

    def test_view_create_article(self):
        client = APIClient()
        data = {
            "email": 'test2@test.com',
            "password": "@TEST1234"
        }
        response = client.post('/users/auth', data)

        data = {
            'use_money': 10000,
            'content': 'test_content',
            'spending_date': '2023-01-12'
        }

        response = client.post('/api/article/', data=data)
        self.assertEquals(response.status_code, 201)

    def test_view_get_user_article_list(self):
        client = APIClient()
        data = {
            "email": 'test2@test.com',
            "password": "@TEST1234"
        }
        response = client.post('/users/auth', data)

        data = {
            'use_money': 10000,
            'content': 'test_content',
            'spending_date': '2023-01-12'
        }

        response = client.post('/api/article/', data=data)
        self.assertEquals(response.status_code, 201)

        response = client.get('/api/article/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()[0]['use_money'], 10000)
        self.assertEquals(response.json()[0]['content'], 'test_content')
        self.assertEquals(response.json()[0]['spending_date'], '2023-01-12')


class ArticleDetailAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('test2@test.com', "@TEST1234")
        cls.test_article = ArticleModels.objects.create(
            writer=user,
            use_money=10000,
            content='test_content',
            spending_date='2023-01-12'
        )

    def test_view_get_article(self):
        print('get_article start')
        pk = self.test_article.id
        client = APIClient()
        data = {
            "email": 'test2@test.com',
            "password": "@TEST1234"
        }
        response = client.post('/users/auth', data)

        response = client.get(f'/api/article/{pk}')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['use_money'], 10000)
        self.assertEquals(response.json()['content'], 'test_content')
        self.assertEquals(response.json()['spending_date'], '2023-01-12')
        print('get_article pass')

    def test_view_update_article(self):
        print('get_update pass')
        pk = self.test_article.id
        client = APIClient()
        data = {
            "email": 'test2@test.com',
            "password": "@TEST1234"
        }
        response = client.post('/users/auth', data)

        data = {
            'use_money': 20000,
            'content': 'test_update',
            'spending_date': '2023-01-11'
        }
        response = client.patch(f'/api/article/{pk}', data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['use_money'], 20000)
        self.assertEquals(response.json()['content'], 'test_update')
        self.assertEquals(response.json()['spending_date'], '2023-01-11')
        print('get_update pass')

    def test_view_delete_article(self):
        pk = self.test_article.id
        client = APIClient()
        data = {
            "email": 'test2@test.com',
            "password": "@TEST1234"
        }
        response = client.post('/users/auth', data)

        response = client.delete(f'/api/article/{pk}')

        self.assertEquals(response.status_code, 204)


class ActionViewSetAndShortUrlTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('test2@test.com', "@TEST1234")
        ArticleModels.objects.create(
            writer=user,
            use_money=10000,
            content='test_content',
            spending_date='2023-01-12'
        )

    def test_view_action_copy(self):
        client = APIClient()
        data = {
            "email": 'test2@test.com',
            "password": "@TEST1234"
        }
        response = client.post('/users/auth', data)

        response = client.post('/api/article/action/1')

        self.assertEquals(response.json()['id'], 2)
        self.assertEquals(response.json()['use_money'], 10000)
        self.assertEquals(response.json()['content'], 'test_content')
        self.assertEquals(response.json()['spending_date'], '2023-01-12')

    def test_view_short_cut(self):
        client = APIClient()
        data = {
            "email": 'test2@test.com',
            "password": "@TEST1234"
        }
        response = client.post('/users/auth', data)

        response = client.get('/api/article/action/1')
        self.assertEquals(bool(response.json()['new_link']), True)
        new_link = response.json()['new_link']

        response = client.get(new_link)
        self.assertEquals(response.json()['use_money'], 10000)
        self.assertEquals(response.json()['content'], 'test_content')
        self.assertEquals(response.json()['spending_date'], '2023-01-12')
