from django.shortcuts import render


def cognito_login(request):
    cognito_domain = os.getenv(
        "COGNITO_DOMAIN", "default_value"
    )  # Replace 'default_value' with a default value or leave it empty
    cognito_client_id = os.getenv("COGNITO_CLIENT_ID", "default_value")
    cognito_redirect_uri = os.getenv("COGNITO_REDIRECT_URI", "default_value")
    cognito_callback_url = os.getenv("COGNITO_CALLBACK_URL", "default_value")
    cognito_aws_region = os.getenv("COGNITO_AWS_REGION", "default_value")

    error_message = None
    return render(
        request,
        "accounts/cognito_login.html",
        {
            "cognito_domain": cognito_domain,
            "cognito_client_id": cognito_client_id,
            "cognito_redirect_uri": cognito_redirect_uri,
            "cognito_aws_region": cognito_aws_region,
            "cognito_callback_url": cognito_callback_url,
            "error_message": error_message,
        },
    )
