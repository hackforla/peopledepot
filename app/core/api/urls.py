from django.urls import path
from rest_framework import routers

from .views import AffiliateViewSet
from .views import AffiliationViewSet
from .views import CheckTypeViewSet
from .views import EventTypeViewSet
from .views import EventViewSet
from .views import FaqViewedViewSet
from .views import FaqViewSet
from .views import LeadershipTypeViewSet
from .views import LocationViewSet
from .views import PermissionTypeViewSet
from .views import PracticeAreaViewSet
from .views import ProgramAreaViewSet
from .views import ProjectStatusViewSet
from .views import ProjectViewSet
from .views import ReferrerTypeViewSet
from .views import ReferrerViewSet
from .views import SdgViewSet
from .views import SkillViewSet
from .views import SocMajorViewSet
from .views import StackElementTypeViewSet
from .views import StackElementViewSet
from .views import UrlTypeViewSet
from .views import UserPermissionViewSet
from .views import UserProfileAPIView
from .views import UserStatusTypeViewSet
from .views import UserViewSet

router = routers.SimpleRouter()
router.register(r"user-permissions", UserPermissionViewSet, basename="user-permission")
router.register(r"users", UserViewSet, basename="user")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"referrer-types", ReferrerTypeViewSet, basename="referrer-type")
router.register(r"referrers", ReferrerViewSet, basename="referrer")
router.register(r"events", EventViewSet, basename="event")
router.register(r"event-types", EventTypeViewSet, basename="event-type")
router.register(r"practice-areas", PracticeAreaViewSet, basename="practice-area")
router.register(r"affiliates", AffiliateViewSet, basename="affiliate")
router.register(r"faqs", FaqViewSet, basename="faq")
router.register(r"faqs-viewed", FaqViewedViewSet, basename="faq-viewed")
router.register(r"leadership-types", LeadershipTypeViewSet, basename="leadership-type")
router.register(r"locations", LocationViewSet, basename="location")
router.register(r"program-areas", ProgramAreaViewSet, basename="program-area")
router.register(r"skills", SkillViewSet, basename="skill")
router.register(r"stack-elements", StackElementViewSet, basename="stack-element")
router.register(r"permission-types", PermissionTypeViewSet, basename="permission-type")
router.register(
    r"stack-element-types", StackElementTypeViewSet, basename="stack-element-type"
)
router.register(r"sdgs", SdgViewSet, basename="sdg")
router.register(
    r"affiliations",
    AffiliationViewSet,
    basename="affiliation",
)
router.register(r"check-types", CheckTypeViewSet, basename="check-type")
router.register(r"project-statuses", ProjectStatusViewSet, basename="project-status")
router.register(r"soc-majors", SocMajorViewSet, basename="soc-major")
router.register(r"url-types", UrlTypeViewSet, basename="url-type")
router.register(
    r"user-status-types", UserStatusTypeViewSet, basename="user-status-type"
)
urlpatterns = [
    path("me/", UserProfileAPIView.as_view(), name="my_profile"),
]

urlpatterns += router.urls
