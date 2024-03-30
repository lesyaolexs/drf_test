from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Group, User
from app.serializers import GroupSerializer, MembershipSerializer, UserSerializer
from app.tasks import clean_db


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the group.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(methods=["post"], detail=False, url_path="add-users", url_name="add_users")
    def add_user(self, request):
        queryset_groups = Group.objects.all()
        get_object_or_404(queryset_groups, pk=request.data["group_id"])
        queryset_users = User.objects.all()
        get_object_or_404(queryset_users, pk=request.data["user_id"])

        add_user_to_group = User.groups.through.objects.create(**request.data)

        response_serializer = MembershipSerializer(add_user_to_group)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=["delete"],
        detail=True,
        url_path="delete-users",
        url_name="delete_users",
    )
    def delete_user(self, request, pk=None):
        queryset = User.groups.through.objects.all()
        user_id = request.data["user_id"]
        group_members = queryset.filter(user_id=user_id)

        group_members.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CleanDBView(APIView):
    """
    ViewSet for deleting all records in db.
    """

    def post(self, request):
        clean_db.apply_async()
        return Response(status=status.HTTP_204_NO_CONTENT)
