# Cognito authentication

## What is it

Cognito is a single sign-on system from AWS. It allows multiple apps to accept authentication from the same set of user accounts. It separates the management of users and permissions from the applications that use them.

## Why we use cognito

We're invested in AWS, so we might as well use this too.

## How we implement it

We're following the implementation from the [djangostar tutorial](https://djangostars.com/blog/bootstrap-django-app-with-cognito/).

These are the steps involved:

1. Backend downloads JWKS from Cognito User Pool on launch
1. User submits credentials and gets id_token and access_token
1. User sends request with token
1. Backend verifies token and processes request
1. User gets response from authenticated API

## Current Dev Setup

1. Created app client called "backend within the vrms-dev user pool, with ALLOW_ADMIN_USER_PASSWORD_AUTH enabled
1. "Domain Name" is already created at [https://hackforla-vrms-dev.auth.us-west-2.amazoncognito.com](https://hackforla-vrms-dev.auth.us-west-2.amazoncognito.com)
1. In "App client settings", enabled Implicit grant and openid, Callback URL [http://localhost:8000/admin](http://localhost:8000/admin)

## How it works now with the dev user pool and local development backend

1. [Create a cognito user](https://hackforla-vrms-dev.auth.us-west-2.amazoncognito.com/login?client_id=3e3bi1ct2ks9rcktrde8v60v3u&response_type=token&scope=openid&redirect_uri=http://localhost:8000/admin) and login from the Hosted UI (from App client settings). Successful login will redirect to localhost:8000/admin with the necessary tokens
1. Take the access_token from the URL and make a GET request to http://localhost:8000/api/v1/me (Headers key=Authorization, value=Bearer <token>)
1. Backend should return the user's profile data

## Notes

The tutorial is 2 years old now (from 2020) and there's been some change made since then.

1. We created an app client in Cognito for the backend to interface with. ALLOW_ADMIN_USER_PASSWORD_AUTH is the new name for the old ADMIN_NO_SRP_AUTH setting. [Reference](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow.html)
1. In the custom User model step, the ugettext-lazy package is gettext-lazy for Django 4.0 [Reference](https://forum.djangoproject.com/t/importerror-cannot-import-name-ugettext-lazy-from-django-utils-translation/10943/3)
1. The tutorial steps don't include instructions to test each step, so it's a little bit of following blindly with the help of linters until the last step.
