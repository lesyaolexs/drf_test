import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.models import CustomUser
from app.serializers import CustomUserSerializer


class CustomUserTest(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create(
            login="user1", sex="male", birth_date="2022-08-06"
        )
        self.user2 = CustomUser.objects.create(
            login="user2", sex="female", birth_date="2022-08-06"
        )
        self.user3 = CustomUser.objects.create(
            login="user3", sex="male", birth_date="2022-08-06"
        )

    def test_users_list(self):
        """
        Ensure that getting all users.
        """
        # get API response
        url = reverse("users-list")
        response = self.client.get(url)

        # get data from db
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_user_retrieve(self):
        """
        Ensure that getting user be id.
        """
        url = reverse("users-detail", kwargs={'pk': self.user1.pk})
        response = self.client.get(url)

        user = CustomUser.objects.get(pk=self.user1.pk)
        serializer = CustomUserSerializer(user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_invalid_user_retrieve(self):
        """
        Ensure that no getting invalid user be id.
        """
        url = reverse("users-detail", kwargs={'pk': uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
