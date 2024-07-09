import secrets

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from core.models import User

CODES = {}  # Temporary storage for codes


class GetCodeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "password": {"type": "string"},
                },
                "required": ["username", "password"],
            }
        },
        responses={
            200: OpenApiResponse(
                response={"type": "object", "properties": {"code": {"type": "string"}}},
                description="Success",
                examples=[
                    OpenApiExample(
                        "Success Response",
                        summary="Example of a successful response",
                        value={"code": "some_generated_code"},
                    )
                ],
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {"error": {"type": "string"}},
                },
                description="Invalid credentials",
                examples=[
                    OpenApiExample(
                        "Error Response",
                        summary="Example of an error response",
                        value={"error": "Invalid credentials"},
                    )
                ],
            ),
        },
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            code = secrets.token_urlsafe(16)

            CODES[code] = user.uuid
            return JsonResponse({"code": code})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)


class GetTokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {"code": {"type": "string"}},
                "required": ["code"],
            }
        },
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {"token": {"type": "string"}},
                },
                description="Success",
                examples=[
                    OpenApiExample(
                        "Success Response",
                        summary="Example of a successful response",
                        value={"token": "some_jwt_token"},
                    )
                ],
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {"error": {"type": "string"}},
                },
                description="Invalid code",
                examples=[
                    OpenApiExample(
                        "Error Response",
                        summary="Example of an error response",
                        value={"error": "Invalid code"},
                    )
                ],
            ),
        },
    )
    def post(self, request):
        code = request.data.get("code")
        uuid = CODES.get(code)
        if uuid:
            user = User.objects.get(uuid=uuid)
            token = jwt.encode(
                {"uuid": str(user.uuid)}, settings.SECRET_KEY, algorithm="HS256"
            )
            return JsonResponse({"token": token})
        else:
            return JsonResponse({"error": "Invalid code"}, status=400)
