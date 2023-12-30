from django.shortcuts import render

def access_denied_view(request):
    return render(request, "custommiddleware/access_denied.html")
