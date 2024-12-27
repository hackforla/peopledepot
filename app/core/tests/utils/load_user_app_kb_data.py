from ..test_user_app_kb_api import UserAppKbApiTestCase
from django.contrib.auth.models import Group
from core.models import User
from rest_framework_jwt.settings import api_settings
from rest_framework.test import APIClient

def load_user_app_kb_data():
        UserAppKbApiTestCase.user = User.objects.create_user(
            username="login-kb-user",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
        )
        UserAppKbApiTestCase.user.set_password("password123")
        UserAppKbApiTestCase.user.save()
        group = Group.objects.get(name__startswith="kb")
        UserAppKbApiTestCase.user.groups.add(group)


        # Generate a JWT token for the user
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(UserAppKbApiTestCase.user)
        UserAppKbApiTestCase.token = jwt_encode_handler(payload)

        # Set the Authorization header for the client
        UserAppKbApiTestCase.kb_client = APIClient()

        UserAppKbApiTestCase.kb_user1 = User.objects.create_user(
            username="kbuser1",
            email="kbuser@example.com",
            first_name="Other",
            last_name="User",
        )
        UserAppKbApiTestCase.kb_user1.groups.add(group)

        # Create additional users
        UserAppKbApiTestCase.other_user = User.objects.create_user(
            username="otheruser",
            email="otheruser@example.com",
            first_name="Other",
            last_name="User",
        )
