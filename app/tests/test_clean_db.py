from django.contrib.auth.models import User as AuthUser
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from app.models import Group, User
from app.tasks import clean_db


class CleanDBTest(APITestCase):

    def setUp(self):
        AuthUser.objects.create_user(
            username='auth_user', email='authuser@mail.com', password='top_secret')
        self.auth_user = AuthUser.objects.first()
        self.client = APIClient()
        self.client.force_authenticate(user=self.auth_user)
        self.group = Group.objects.create(name="group", public=True)
        self.user = User.objects.create(login="user", sex="male", birth_date="2022-08-08")

    def test_clean_db(self):
        url = "/app/cleanup/"
        response = self.client.post(url)
        task = clean_db.apply()
        all_records = User.objects.prefetch_related("groups")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(task.successful())
        self.assertFalse(all_records.exists())
