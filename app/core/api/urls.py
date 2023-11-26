from django.urls import path
from rest_framework import routers
from django.views.generic import TemplateView
from .views import SecureApiView


from .views import EventViewSet
from .views import FaqViewedViewSet
from .views import FaqViewSet
from .views import LocationViewSet
from .views import PermissionTypeViewSet
from .views import PracticeAreaViewSet
from .views import ProgramAreaViewSet
from .views import ProjectViewSet
from .views import SkillViewSet
from .views import SponsorPartnerViewSet
from .views import TechnologyViewSet
from .views import UserProfileAPIView
from .views import UserViewSet
# from .views import no_staff_access

router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"events", EventViewSet, basename="event")
router.register(r"practice-areas", PracticeAreaViewSet, basename="practice-area")
router.register(r"sponsor-partners", SponsorPartnerViewSet, basename="sponsor-partner")
router.register(r"faqs", FaqViewSet, basename="faq")
router.register(r"faqs-viewed", FaqViewedViewSet, basename="faq-viewed")
router.register(r"locations", LocationViewSet, basename="location")
router.register(r"program-areas", ProgramAreaViewSet, basename="program-area")
router.register(r"skills", SkillViewSet, basename="skill")
router.register(r"technologies", TechnologyViewSet, basename="technology")
router.register(r"permission-types", PermissionTypeViewSet, basename="permission-type")

urlpatterns = [
    path('secure-api/', SecureApiView.as_view(), name='secure_api'),
    path('me/', UserProfileAPIView.as_view(), name='my_profile'),
    path('home/', TemplateView.as_view(template_name='common/home.html'), name='home'),
    # path('no_staff_access/', no_staff_access, name='no_staff_access'),
]

urlpatterns += router.urls
