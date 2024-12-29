def filter_user_queryset(request, queryset):
    email = request.query_params.get("email")
    if email is not None:
        queryset = queryset.filter(email=email)
    username = request.query_params.get("username")
    if username is not None:
        queryset = queryset.filter(username=username)
    return queryset
