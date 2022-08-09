from django.urls import path
from rest_framework import routers

from .views import ProjectViewSet, UserProfileAPIView, UserViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"projects", ProjectViewSet, basename="project")

urlpatterns = [
    path("me/", UserProfileAPIView.as_view(), name="my_profile"),
]

urlpatterns += router.urls
