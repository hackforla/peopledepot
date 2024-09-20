# from rest_framework import serializers as rest_serializers
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_api_key.permissions import HasAPIKey

from core.api.serializers import PracticeAreaSerializer
from core.api.serializers import UserSerializer
from core.models import PracticeArea
from core.models import User


@extend_schema_view(
    list=extend_schema(
        description="""
Lists all users and the associated groups for the user

Requires
- API keys have been added using the API key screen in the People depot App.
Check with People Depot admin.
- Requires X-Api-Key be set when submitting request
For curl, it would look like this:
```http
curl -L -X GET "localhost:8001/api/v1/apikey/getusers/"
-H "X-Api-Key: *************"
-H "Content-Type: application/json"
```


For python, it would look like this:
```bash
import requests

API_KEY = os.environ.get("API_KEY")
BASE_URL = "http:8000"
HEADERS = {
    'X-Api-Key': API_KEY,
    'Content-Type': 'application/json'
}
response = requests.get(f"{BASE_URL}/api/v1/apikey/getusers/", headers=HEADERS)
```
        """
    )
)
class ApiKeyUserViewSet(viewsets.ReadOnlyModelViewSet):
    # HasAPIKey checks if value of X-API-KEY is in API keys table
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKey]
    queryset = PracticeArea.objects.all()
    serializer_class = PracticeAreaSerializer  # HasAPIKey checks against keys stored in
    queryset = User.objects.all()

    # when instantiated, get_serializer_context will be called
    serializer_class = UserSerializer

    # get_serializer_context called to set include_groups to True
    # to include groups in the response
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["include_groups"] = True
        return context
