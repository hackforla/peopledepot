# Cognito authentication workflow (pre deployment)

This is a temporary solution until we can deploy a dev environment for PeopleDepot.

There's a few manual steps and the login is good for only an hour at a time.

Prerequisites:

- [ModHeader](https://modheader.com/modheader/download) browser extension

Steps:

1. Login (or register first then login) to a cognito account [here](https://hackforla-vrms-dev.auth.us-west-2.amazoncognito.com/login?client_id=3e3bi1ct2ks9rcktrde8v60v3u&response_type=token&scope=openid&redirect_uri=http://localhost:8000/admin). Do not worry if you see error messages - you will be using the url.

    [<img src="https://user-images.githubusercontent.com/1160105/184449364-e3bba6e9-ced5-498f-a0e6-0c93c8a036fb.png" width="500" />](https://user-images.githubusercontent.com/1160105/184449364-e3bba6e9-ced5-498f-a0e6-0c93c8a036fb.png)

1. Copy the URL when it redirects. **Note:** Instead of the screen below, the screen may display an error message. You can ignore any error messages.

    [<img src="https://user-images.githubusercontent.com/1160105/184449368-f16b19de-9372-436c-b65d-c5afadbcbc1a.png" width="500" />](https://user-images.githubusercontent.com/1160105/184449368-f16b19de-9372-436c-b65d-c5afadbcbc1a.png).

1. Extract the `access_token` using the [online tool](https://regexr.com/6ro69).

    1. Clear the top box and paste the URL text into it. The box should show there's 1 match
    1. The bottom box's content is the extracted `access_token`

    [<img src="https://user-images.githubusercontent.com/1160105/184449537-2a9570a5-6361-48ae-b348-506244d592ac.png" width="500" />](https://user-images.githubusercontent.com/1160105/184449537-2a9570a5-6361-48ae-b348-506244d592ac.png)

1. Open [ModHeader](https://modheader.com/modheader/download). If the icon is hidden, click on the Puzzle icon in the upper right of the browser to see it.

1. Type the word Bearer and paste the token into [ModHeader](https://docs.modheader.com/using-modheader/introduction) Authorization: Bearer \<access_token>

    [<img src="https://user-images.githubusercontent.com/1160105/184449582-3de548f4-769b-43ac-82b3-06ec2845ead2.png" width="500" />](https://user-images.githubusercontent.com/1160105/184449582-3de548f4-769b-43ac-82b3-06ec2845ead2.png)

1. Go to a page in api/v1/ to see that it allows access

    [<img src="https://user-images.githubusercontent.com/1160105/184449777-36f95985-9e19-4010-ba5f-6f9eb3324c2b.png" width="500" />](https://user-images.githubusercontent.com/1160105/184449777-36f95985-9e19-4010-ba5f-6f9eb3324c2b.png)

1. Explore APIs using [Swagger](http://localhost:8000/api/schema/swagger-ui)

    [<img src="https://user-images.githubusercontent.com/1160105/184449905-43a95335-20b8-4bf4-8a1b-10b95b7c48be.png" width="500" />](https://user-images.githubusercontent.com/1160105/184449905-43a95335-20b8-4bf4-8a1b-10b95b7c48be.png)

1. Some fields have hints on how to retrieve the values.

    [<img src="https://user-images.githubusercontent.com/1160105/184449693-a4b9a0e8-75b2-41f0-b52d-83c8c2c4ac20.png" width="500" />](https://user-images.githubusercontent.com/1160105/184449693-a4b9a0e8-75b2-41f0-b52d-83c8c2c4ac20.png)

1. A redoc ui is also available

    [<img src="https://user-images.githubusercontent.com/1160105/184450043-eb1e4af8-f957-4e85-8959-6863fb1f04bf.png" width="500" />](https://user-images.githubusercontent.com/1160105/184450043-eb1e4af8-f957-4e85-8959-6863fb1f04bf.png)
