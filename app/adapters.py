# myapp/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpResponse
import logging

# Set up logging
logger = logging.getLogger(__name__)

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def on_authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        # Log error details
        
        logger.error(   format(request))
        logger.error(f"Authentication error debug: {error}, Exception: {exception}")
        return HttpResponse("Custom error message", status=400)
