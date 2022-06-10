from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """Used to retrieve user info"""

    class Meta:
        model = User
        fields = "__all__"
