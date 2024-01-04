This document covers how to sign up for a Cognito User Pool account in development through the People Depot
App.  This is not to be confused with a Cognito account- the Cognito User Pool account is specific to the configured user pool.  Amazon places restrictions on how you sign up for a user pool account if generic public (vs org specific) emails are allowed.

You can sign up with or without a verified SES Amazon email.  

## Verifying SES Amazon Email

Signing up with an SES Amazon email requires that a Cognito admin submits you as an SES Authorized Email sender.  An admin can do this from https://<region>.console.aws.amazon.com/ses?region=<region>#/verified-identities (or clicking on Get Started=> Verify Email from the SES console home page) and then
entering your email.  You will then get an email with a link to click on.  

## Signing up from People Depot
You can use a verified SES Amazon email if you have one (see previous section).

  - sign up for an account from URL http://localhost:8000/accounts/login.  A Cognito sign in screen with a Continue button will be displayed.
  - click on Continue.  An Amazon Cognito sign in screen will be displayed.
  - Click on Sign Up.  An Amazon Cognito sign up screen will be displayed.  
  - enter your email address and a password for that account.  Press submit.  A screen will prompt you to enter a verification code.
  - open up your email to get the verification code.
  - enter the verification code and press enter.

If you used a verified SES Amazon email the People Depot screen will appear with a message that you need an admin to assign you roles.

If you did not use a verified SES Amazon email you will get an error message that there was an error with the SES email verification.  If this is the case, continue to the next section.

## Confirming an account that is not a verified Amazon SES email
An admin can confirm accounts that are not verified by using this URL and selecting Confirm Account option.

## Creating multiple Cognito user pool accounts with one Gmail account
Gmail provides two mechanisms for using different email addresses that are associated with the samegmail account.  You can put a period (.) anywhere is the username, e.g. john.doe@gmail.com, j.ohnd.oe@gmail.com and johndoe@gmail.com all refer to the same gmail account.  You can also append a plus (+) to the username and follow it with any characters, e.g. john.doe+a1@gmail.com.  

If you have verified an email for the Gmail account, regardless of added punctionation, Cognito will prompt you to enter a verification code and will send you an email with the verification code.
