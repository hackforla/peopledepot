from django.urls import path
from rest_framework import routers

from .views import (
    ProjectViewSet,
    RecurringEventViewSet,
    SponsorPartnerViewSet,
    UserProfileAPIView,
    UserViewSet,
)

router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"recurring-events", RecurringEventViewSet, basename="recurring-event")
router.register(r"sponsor-partners", SponsorPartnerViewSet, basename="sponsor-partner")

urlpatterns = [
    path("me/", UserProfileAPIView.as_view(), name="my_profile"),
]

urlpatterns += router.urls
