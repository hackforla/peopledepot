from django.urls import path
from rest_framework import routers

from .views import UserProfileAPIView, UserViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("me/", UserProfileAPIView.as_view(), name="my_profile"),
]

urlpatterns += router.urls
