from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from app.models import CustomUser
from app.serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing, retrieving, creating,
    partial updating, destroying users.
    """

    def list(self, request) -> Response:
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None) -> Response:
        queryset = CustomUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def create(self, request) -> Response:
        request_serializer = CustomUserSerializer(data=request.data)

        request_serializer.is_valid(raise_exception=True)
        created_user = CustomUser.objects.create(**request_serializer.data)
        response_serializer = CustomUserSerializer(created_user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        queryset = CustomUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = CustomUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        response_serializer = CustomUserSerializer(user)
        user.delete()
        return Response(response_serializer.data)
