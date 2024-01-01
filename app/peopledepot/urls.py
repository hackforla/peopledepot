from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic.base import TemplateView
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # below line required so that when a user with is_staff=False tries for 
    # admin/login page to be redirected to the accounts/login page
    # If you comment out the below line, then when a user with is_staff=False 
    # clicks on logout page they are redirected to admin/login instead of
    # accounts/login.  This is because admin/logout uses allauth logout view
    # which does not work with next field (admin/logout/?next=/accounts/login/)
    path('admin/logout/', auth_views.LogoutView.as_view(), name='admin_logout'),

    path("admin/", admin.site.urls),
    path("api/v1/", include("core.api.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "no_admin_access/",
        TemplateView.as_view(template_name="admin/no_admin_access.html"),
        name="no_admin_access",
    ),
    path("accounts/", include("allauth.urls")),
]
