"""peopledepot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from core.api.views import (
    UserListCreateAPIView,
    UserProfileAPIView,
    UserRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/me", UserProfileAPIView.as_view(), name="my_profile"),
    path("api/v1/users/", UserListCreateAPIView.as_view(), name="users_list"),
    path(
        "api/v1/users/<uuid:uuid>/",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="users",
    ),
]
