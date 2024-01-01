from django.shortcuts import redirect, render
from django.contrib.auth import views as auth_views


def access_denied_view(request):
    return render(request, "custommiddleware/access_denied.html")

class CustomLogoutView(auth_views.LogoutView):
    def get(self, request, *args, **kwargs):
        # Call the super() method to get the standard LogoutView behavior
        super().get(request, *args, **kwargs)
        return redirect("/admin/login/")
