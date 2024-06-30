### Pre-requisites
- A Cognito user pool and client has been set up using Amazon Cognito
- 

- You know the values for the following variables.  Values that should work for dev are set below.  You will need to get the COGNITO_CLIENT_ID and COGNITO_CLIENT_SECRET from a lead.
```
COGNITO_DOMAIN=peopledepot
COGNITO_AWS_REGION=us-west-2
COGNITO_USER_POOL=us-west-2_Fn4rkZpuB
COGNITO_CLIENT_ID=xxxxxxx - ask a lead for the client id for dev
COGNITO_CLIENT_SECRET= - blank for dev
```

### Setting up for development
Modify .env.docker or .env.local to include the variables mentioned above.  Also, include: `COGNITO_CALLBACK_URL=http://localhost:8000/accounts/amazon-cognito/login/callback/`

### Setting Up Test or Development
Set up a cognito user pool and domain in Amazon Cognito,if not done.  Specify values for variables in github variables.
