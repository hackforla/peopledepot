import os
import time
import requests

from ..models import User
from rest_framework.generics import GenericAPIView
from django.views.decorators.csrf import csrf_exempt
from core.models import User
import hashlib
import hmac
import time
from django.http import JsonResponse
from django.core import serializers

API_SECRET=os.environ.get('API_SECRET')

MAX_TOLERANCE_SECONDS=10

def is_expected_signature(request):
        api_key = request.headers.get('X-API-Key', '')
        timestamp = request.headers.get('X-API-Timestamp', '')
        signature = request.headers.get('X-API-Signature', '')

        current_timestamp = str(int(time.time()))
        if abs(int(timestamp) - int(current_timestamp)) > 10:
            return JsonResponse({'error': 'Invalid timestamp'}, status=400)
        print("api_key", api_key, "timestamp", timestamp, "signature", signature)

        # Recreate the message and calculate the expected signature
        expected_signature = hmac.new(API_SECRET.encode('utf-8'), f"{timestamp}{api_key}".encode('utf-8'), hashlib.sha256).hexdigest()
        return(signature == expected_signature)
 

class SecureCreateUser(GenericAPIView):
    permission_classes=[]
    @csrf_exempt
    def post(self, request: requests):
        print("posting create user")
        is_signature_matched = is_expected_signature(request)
        print("signature matches", is_signature_matched)

        # Compare the calculated signature with the one sent in the request
        if is_signature_matched:
            # Signature is valid, process the request
            data = request.POST
            username = data.get("username")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            email = data.get("email") 
            print("Updating user")       
            User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
            return JsonResponse({'message': 'API call successful', 'data': request.data, 'user': data})
        else:
            # Invalid signature, reject the request
            return JsonResponse({'error': 'Invalid signature'}, status=401)


class SecureGetUsers(GenericAPIView):
    permission_classes=[]
    @csrf_exempt
    def get(self, request: requests):
        is_signature_matched = is_expected_signature(request)

        # Compare the calculated signature with the one sent in the request
        if is_signature_matched:
            # Signature is valid, process the request
            user_data = serializers.serialize("json", User.objects.all())
            return JsonResponse({'message': 'API call successful', 'data': request.data, 'users': user_data})
        else:
            # Invalid signature, reject the request
            return JsonResponse({'error': 'Invalid signature'}, status=401)

