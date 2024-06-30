# from rest_framework import serializers as rest_serializers
from core.api.secret_permissions import HasValidSignature
from rest_framework import viewsets

from core.api.serializers import UserSerializer
from core.models import User

class SecretUserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [HasValidSignature]
    queryset = User.objects.all()
    # when instantiated, get_serializer_context will be called
    serializer_class = UserSerializer

    # get_serializer_context called to set include_groups to True
    # to include groups in the response
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['include_groups'] = True
        return context  