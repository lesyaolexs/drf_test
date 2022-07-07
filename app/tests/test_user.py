import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.models import User
from app.serializers import UserSerializer


class UserTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            login="user1", sex="male", birth_date="2022-08-06"
        )
        self.user2 = User.objects.create(
            login="user2", sex="female", birth_date="2022-08-06"
        )
        self.user3 = User.objects.create(
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
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_user_retrieve(self):
        """
        Ensure that getting user by id.
        """
        url = reverse("users-detail", kwargs={'pk': self.user1.pk})
        response = self.client.get(url)

        user = User.objects.get(pk=self.user1.pk)
        serializer = UserSerializer(user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_invalid_user_retrieve(self):
        """
        Ensure that no getting invalid user by id.
        """
        url = reverse("users-detail", kwargs={'pk': uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user(self):
        """
        Ensure that creating user.
        """

        url = reverse("users-list")
        data = {
            "login": "user4",
            "sex": "female",
            "birth_date": "2022-08-06"
        }
        records_number = User.objects.count()

        response = self.client.post(url, data=data, format="json")
        created_user = User.objects.get(pk=response.data["id"])
        serializer = UserSerializer(created_user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), records_number + 1)
        self.assertEqual(response.data, serializer.data)

    def test_invalid_user_create(self):
        """
        Ensure that creating correct user.
        """

        url = reverse("users-list")
        invalid_data = {
            "login": "5userinvalidsolong",
            "sex": "fXemale",
            "birth_date": "202208-06"
        }

        valid_response = {
            "login": [" Login must starts with a letter", "Ensure this field has no more than 16 characters."],
            "sex": ["\"fXemale\" is not a valid choice."],
            "birth_date": ["Date has wrong format. Use one of these formats instead: YYYY-MM-DD."]}

        response = self.client.post(url, data=invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, valid_response)

    def test_partial_update_user(self):
        """
        Ensure that user partial updating by id.
        """
        url = reverse("users-detail", kwargs={'pk': self.user1.pk})
        data = {
            "login": "userUpdated",
            "sex": "male",
        }

        response = self.client.patch(url, data=data, format="json")
        updated_user = User.objects.get(pk=response.data["id"])
        serializer = UserSerializer(updated_user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete_user(self):
        """
        Ensure that user deleting by id.
        """

        url = reverse("users-detail", kwargs={'pk': self.user1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_user(self):
        """
        Ensure that user correct deleting by id.
        """

        url = reverse("users-detail", kwargs={'pk': uuid.uuid4()})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
