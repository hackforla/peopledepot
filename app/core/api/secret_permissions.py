import hashlib
import hmac
import time

from core.constants import message_invalid_signature
from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from django.conf import settings


class _ApiFields:
    def __init__(self, api_key: str, timestamp: str, signature: str):
        self.api_key = api_key
        self.timestamp = timestamp
        self.signature = signature


def _get_request_api_fields(request) -> _ApiFields:
    api_key = request.headers.get("X-API-Key", "")
    timestamp = request.headers.get("X-API-Timestamp", "")
    signature = request.headers.get("X-API-Signature", "")
    return _ApiFields(api_key=api_key, timestamp=timestamp, signature=signature)


def _is_expected_signature(api_key: str, timestamp: str, signature: str) -> bool:
    current_timestamp = int(time.time())
    request_timestamp = int(timestamp)
    if abs(current_timestamp - request_timestamp) > 10:
        return False

    # Recreate the message and calculate the expected signature
    message = f"{timestamp}{api_key}"
    expected_signature = hmac.new(
        settings.SECRET_API_KEY.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(signature, expected_signature)


def _has_expected_request_signature(request) -> bool:
    api_fields = _get_request_api_fields(request)
    return _is_expected_signature(
        api_fields.api_key, api_fields.timestamp, api_fields.signature
    )


class HasValidSignature(BasePermission):
    def has_permission(self, request, __view__) -> bool:
        if not _has_expected_request_signature(request):
            raise PermissionDenied(message_invalid_signature)
        return True

    def has_object_permission(self, request, __view__, __obj__) -> bool:
        if not _has_expected_request_signature(request):
            raise PermissionDenied(message_invalid_signature)
        return True
        return _has_expected_request_signature(request)
