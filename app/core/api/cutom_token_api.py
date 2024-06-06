from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

import jwt
from 

def generate_token(user, rsa_keys):
    """
    Generate a JWT token for the given user, including the user's UUID in the payload.
    """
    print(api_settings.JWT_P)
    # Ensure the user object has a UUID attribute
    user_uuid = str(user.uuid)

    # Create the payload
    payload = {
        'user_id': user_uuid,
        # Add any other custom claims here
    }

    # Get the appropriate RSA key for signing based on your key ID
    key_id = 'your_key_id'  # Replace with your actual key ID
    private_key = rsa_keys[key_id]

    # Generate the token
    token = jwt.encode(payload, private_key, algorithm='RS256', headers={'kid': key_id})

    # Return the token as a string
    return token


class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        print("debug for_user2", user)
        if user:
            print("debug for_user", user.__dict__)
        token = super().for_user(user)
        print("Here we are again")
        token['user_id'] = str(user.uuid)
        print("Made it to here", token['user_id'])
        return token

    def get_user_id(self):
        """
        Override get_user_id method to return the UUID of the user instead of the ID.
        """
        print("Here we are 2", self.payload,"Done")
        return str(self.payload['user_id'])
    
class CustomTokenSerializer(serializers.Serializer):
    print("Debug CustomTokenSerializer")
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            print("Validating user", username, password)
            user = authenticate(username=username, password=password)
            setattr(user, 'id', user.uuid)
            try:
                return generate_token(username, password)
            except Exception as e:
                print("Error generating token", e)
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg)
        attrs['user_id'] = str(user.uuid)
        attrs['token'] = tokens['access']
        return attrs

class CustomTokenObtainView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print("Obtaining token", request.data)
        serializer = CustomTokenSerializer(data=request.data)
        if serializer.is_valid():
            # Perform token creation logic here
            # For example, you can use JWT or any other token mechanism
            # Here, we'll just return a success response with the user_id
            return Response({'user_id': serializer.validated_data['user_id'], 'token': serializer.validated_data['token']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


