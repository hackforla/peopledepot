This document covers how to set up a new Cognito User Pool and corresponding client app.  This information is needed if (1) you are implementing Cognito in production or pre-production environment or (2) you are a developer working on an issue that requires you modify or add Cognito configuration.  

For development, using local accounts is preferred, as it is easier.  If you are working on something that related to Cognito that does not require Cognito configuration modification, you can use existing Cognito credentials set up for People Depot.

The following steps come from https://docs.allauth.org/en/latest/socialaccount/providers/amazon_cognito.html:

1. Go to your https://console.aws.amazon.com/cognito/ and create a Cognito User Pool if you haven’t already.

2. Go to General Settings > App Clients section and create a new App Client if you haven’t already. Please make sure you select the option to generate a secret key.

3. Go to App Integration > App Client Settings section and:

  - Enable Cognito User Pool as an identity provider.
  - Set the callback URls to:
    ```
    localhost:8000/admin/
    localhost:8000/accounts/amazon-cognito/login/callback/
    ```
    NOTE: MAKE SURE TO INCLUDE TRAILING SLASH
  - Enable Authorization Code Grant OAuth flow if not enabled.
  - Set OpenID Connect Scopes to OPENID, EMAIL, and PROFILE

4. Go to App Integration > Domain Name section and create a domain prefix for your Cognito User Pool.
