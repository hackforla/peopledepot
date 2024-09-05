import hashlib
import hmac
import time

from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from core.constants import message_invalid_signature


# Called by _has_expected_request_signature
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


# Called by HasValidSignature
def _has_expected_request_signature(request) -> bool:
    api_key = request.headers.get("X-API-Key", "")
    timestamp = request.headers.get("X-API-Timestamp", "")
    signature = request.headers.get("X-API-Signature", "")
    return _is_expected_signature(api_key, timestamp, signature)


class HasValidSignature(BasePermission):
    def has_permission(self, request, __view__) -> bool:
        if not _has_expected_request_signature(request):
            raise PermissionDenied(message_invalid_signature)
        return True

    def has_object_permission(self, request, __view__, __obj__) -> bool:
        if not _has_expected_request_signature(request):
            raise PermissionDenied(message_invalid_signature)
        return True
