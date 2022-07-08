from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import Group, Membership, User
from app.serializers import (
    GroupSerializer,
    MembershipSerializer,
    MembershipUserSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing, retrieving, creating,
    partial updating, destroying users.
    """

    def list(self, request) -> Response:
        queryset = User.objects.all()
        serializer = MembershipUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None) -> Response:
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request) -> Response:
        request_serializer = UserSerializer(data=request.data)

        request_serializer.is_valid(raise_exception=True)
        created_user = User.objects.create(**request_serializer.data)
        response_serializer = UserSerializer(created_user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing, retrieving, creating,
    partial updating, destroying groups and adding/removing users from group.
    """

    def list(self, request) -> Response:
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None) -> Response:
        queryset = Group.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def create(self, request) -> Response:
        request_serializer = GroupSerializer(data=request.data)

        request_serializer.is_valid(raise_exception=True)
        created_group = Group.objects.create(**request_serializer.data)
        response_serializer = GroupSerializer(created_group)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        queryset = Group.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        serializer = GroupSerializer(group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = Group.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=False, url_path="add-users", url_name="add_users")
    def add_user(self, request):
        queryset_groups = Group.objects.all()
        get_object_or_404(queryset_groups, pk=request.data["group_id"])
        queryset_users = User.objects.all()
        get_object_or_404(queryset_users, pk=request.data["user_id"])

        add_user_to_group = Membership.objects.create(**request.data)

        response_serializer = MembershipSerializer(add_user_to_group)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
