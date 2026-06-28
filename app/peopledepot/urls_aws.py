from django.contrib import admin
from django.http import HttpResponse
from django.urls import include
from django.urls import path


def index(request):
    return HttpResponse("You're at the peopledepot index.")


urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
    path("api/v1/", include("core.api.urls")),
]
