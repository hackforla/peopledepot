import os
import time
import requests

from core.api.secure_serializers import SecureUserSerializer

from ..models import User
from django.contrib.auth.models import Group
from rest_framework.generics import GenericAPIView
from django.views.decorators.csrf import csrf_exempt
from core.models import User
import hashlib
import hmac
import time
from django.http import JsonResponse

# from rest_framework import serializers as rest_serializers
from rest_framework import serializers, viewsets
from django.core import serializers

API_SECRET = os.environ.get("API_SECRET")

MAX_TOLERANCE_SECONDS = 10


def is_expected_signature(request):
    api_key = request.headers.get("X-API-Key", "")
    timestamp = request.headers.get("X-API-Timestamp", "")
    signature = request.headers.get("X-API-Signature", "")

    current_timestamp = str(int(time.time()))
    if abs(int(timestamp) - int(current_timestamp)) > 10:
        return JsonResponse({"error": "Invalid timestamp"}, status=400)
    print("api_key", api_key, "timestamp", timestamp, "signature", signature)

    # Recreate the message and calculate the expected signature
    expected_signature = hmac.new(
        API_SECRET.encode("utf-8"), f"{timestamp}{api_key}".encode(), hashlib.sha256
    ).hexdigest()
    return signature == expected_signature


class SecureCreateUser(GenericAPIView):
    permission_classes = []

    @csrf_exempt
    def post(self, request: requests):
        print("posting create user")
        is_signature_matched = is_expected_signature(request)
        print("signature matches", is_signature_matched)

        # Compare the calculated signature with the one sent in the request
        if is_signature_matched:
            # Signature is valid, process the request
            data = request.POST
            uuid = data.get("uuid")
            username = data.get("username")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            email = data.get("email")
            print("Updating user")
            if not User.objects.filter(uuid=uuid).exists():
                User.objects.create(
                    uuid=uuid,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )
            return JsonResponse(
                {"message": "API call successful", "data": request.data, "user": data}
            )
        else:
            # Invalid signature, reject the request
            return JsonResponse({"error": "Invalid signature"}, status=401)


class SecureUserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = SecureUserSerializer


class SecureGetUsers(GenericAPIView):
    permission_classes = []

    @csrf_exempt
    def get(self, request: requests):
        group_fields = "name"

        # Compare the calculated signature with the one sent in the request
        if is_expected_signature(request):
            user_data = serializers.serialize("json", User.objects.all())
            group_data = serializers.serialize(
                "json", Group.objects.all(), fields=group_fields
            )
            return JsonResponse(
                {
                    "message": "API call successful",
                    "data": request.data,
                    "users": user_data,
                    "groups": group_data,
                }
            )
        else:
            # Invalid signature, reject the request
            return JsonResponse({"error": "Invalid signature"}, status=401)
