from rest_framework import serializers

from app.models import Group, User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="id", required=False
    )

    class Meta:
        model = User
        fields = "__all__"


class MembershipSerializer(serializers.Serializer):
    group_id = serializers.UUIDField()
    user_id = serializers.UUIDField()
