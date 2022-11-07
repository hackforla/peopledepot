from django.urls import path
from rest_framework import routers

from .views import (
    Faq_viewedViewSet,
    FaqViewSet,
    ProjectViewSet,
    RecurringEventViewSet,
    UserProfileAPIView,
    UserViewSet,
)

router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"recurring-events", RecurringEventViewSet, basename="recurring-event")
router.register(r"faqs", FaqViewSet, basename="faq")
router.register(r"faqs_viewed", Faq_viewedViewSet, basename="faq_viewed")

urlpatterns = [
    path("me/", UserProfileAPIView.as_view(), name="my_profile"),
]

urlpatterns += router.urls
