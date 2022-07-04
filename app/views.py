from django.core.handlers.wsgi import WSGIRequest
from rest_framework import viewsets
from rest_framework.response import Response

from app.models import CustomUser
from app.serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing users.
    """

    def list(self, request: WSGIRequest) -> Response:
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)
