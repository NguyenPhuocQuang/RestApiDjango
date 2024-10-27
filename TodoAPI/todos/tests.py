from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Todo


class TodoViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.todo = Todo.objects.create(title='Initial Todo', completed=False,description='Description in Todo')

    def test_create_todo_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        data = {'title': 'New Todo', 'completed': False}
        response = self.client.post(reverse('todo-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_todos_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        response = self.client.get(reverse('todo-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_todo_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        response = self.client.get(reverse('todo-detail', kwargs={'pk': self.todo.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_todo_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        data = {'title': 'Updated Todo', 'completed': True}
        response = self.client.put(reverse('todo-detail', kwargs={'pk': self.todo.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.completed)

    def test_delete_todo_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        response = self.client.delete(reverse('todo-detail', kwargs={'pk': self.todo.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

