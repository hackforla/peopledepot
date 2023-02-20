from django.urls import path
from rest_framework import routers

from .views import FaqViewSet
from .views import FaqViewedViewSet
from .views import ProjectViewSet
from .views import RecurringEventViewSet
from .views import SponsorPartnerViewSet
from .views import UserProfileAPIView
from .views import UserViewSet
from .views import LocationViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"recurring-events", RecurringEventViewSet, basename="recurring-event")
router.register(r"sponsor-partners", SponsorPartnerViewSet, basename="sponsor-partner")
router.register(r"faqs", FaqViewSet, basename="faq")
router.register(r"faqs-viewed", FaqViewedViewSet, basename="faq-viewed")
router.register(r"location", LocationViewSet, basename="location")

urlpatterns = [
    path("me/", UserProfileAPIView.as_view(), name="my_profile"),
]

urlpatterns += router.urls
