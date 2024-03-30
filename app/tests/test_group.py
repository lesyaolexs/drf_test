import uuid

from django.contrib.auth.models import User as AuthUser
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from app.models import Group, User
from app.serializers import GroupSerializer


class GroupTest(APITestCase):

    def setUp(self):
        AuthUser.objects.create_user(
            username='auth_user', email='authuser@mail.com', password='top_secret')
        self.auth_user = AuthUser.objects.first()
        self.client = APIClient()
        self.client.force_authenticate(user=self.auth_user)

        self.group1 = Group.objects.create(name="group1", public=True)
        self.group2 = Group.objects.create(name="group2", public=False)
        self.group3 = Group.objects.create(name="group3", public=True)
        self.user = User.objects.create(login="user", sex="male", birth_date="2022-08-08")

    def test_groups_list(self):
        """
        Ensure that getting all groups.
        """
        # get API response
        url = reverse("groups-list")
        response = self.client.get(url)

        # get data from db
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_group_retrieve(self):
        """
        Ensure that getting group by id.
        """
        url = reverse("groups-detail", kwargs={'pk': self.group1.pk})
        response = self.client.get(url)

        group = Group.objects.get(pk=self.group1.pk)
        serializer = GroupSerializer(group)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_invalid_group_retrieve(self):
        """
        Ensure that no getting invalid group by id.
        """
        url = reverse("groups-detail", kwargs={'pk': uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_group(self):
        """
        Ensure that creating group.
        """

        url = reverse("groups-list")
        data = {
            "name": "group4",
            "public": True
        }
        records_number = Group.objects.count()

        response = self.client.post(url, data=data, format="json")
        created_group = Group.objects.get(pk=response.data["id"])
        serializer = GroupSerializer(created_group)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), records_number + 1)
        self.assertEqual(response.data, serializer.data)

    def test_invalid_group_create(self):
        """
        Ensure that creating correct group.
        """

        url = reverse("groups-list")
        invalid_data = {
            "name": "5groupinvalidsolong",
            "public": "NoBool"
        }

        valid_response = {
            "name": [
                "Login should start with a letter and be alphanumeric",
                "Ensure this field has no more than 16 characters."],
            "public": ["Must be a valid boolean."]
        }

        response = self.client.post(url, data=invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, valid_response)

    def test_partial_update_group(self):
        """
        Ensure that group partial updating by id.
        """
        url = reverse("groups-detail", kwargs={'pk': self.group1.pk})
        data = {"name": "groupUpdated"}

        response = self.client.patch(url, data=data, format="json")
        updated_group = Group.objects.get(pk=response.data["id"])
        serializer = GroupSerializer(updated_group)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete_group(self):
        """
        Ensure that group deleting by id.
        """

        url = reverse("groups-detail", kwargs={'pk': self.group1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_group(self):
        """
        Ensure that group correct deleting by id.
        """

        url = reverse("groups-detail", kwargs={'pk': uuid.uuid4()})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_user(self):
        """
        Ensure that user adding to group.
        """

        url = reverse("groups-add_users")
        group_id = self.group3.pk.__str__()
        user_id = self.user.pk.__str__()
        data = {
            "group_id": group_id,
            "user_id": user_id
        }

        records_number = User.groups.through.objects.count()

        response = self.client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.groups.through.objects.count(), records_number + 1)

    def test_delete_user(self):
        """
        Ensure that user deleting from group.
        """
        url = reverse("groups-delete_users", kwargs={'pk': self.group2.pk})
        user_id = self.user.pk
        data = {
            "user_id": user_id
        }
        response = self.client.delete(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
