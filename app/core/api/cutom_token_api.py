from django.contrib.auth import authenticate
from django.urls import path
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class CustomTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                # Add the user's UUID to the token payload
                attrs["user_id"] = str(user.uuid)
                return attrs
            else:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg)


class CustomTokenObtainView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomTokenSerializer(data=request.data)
        if serializer.is_valid():
            # Perform token creation logic here
            # For example, you can use JWT or any other token mechanism
            # Here, we'll just return a success response with the user_id
            return Response(
                {"user_id": serializer.validated_data["user_id"]},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
