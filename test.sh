# curl --request POST \
#   --url https://peopledepot.auth.us-east-2.amazoncognito.com/oauth2/token \
#   --header 'Content-Type: application/x-www-form-urlencoded' \
#   --data 'grant_type=authorization_code' \
#   --data 'client_id=35ehknpgi8ul8nfn2undd6ufro' \
#   --data 'code=41bf24e-f8e5-49e4-bd0c-983cbd2a30d6' \
#   --data 'redirect_uri=http://localhost:8000/accounts/amazon-cognito/login/callback/'

curl -X POST \
  'https://your-cognito-domain/oauth2/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=authorization_code' \
  -d 'client_id=your-client-id' \
  -d 'client_secret=your-client-secret' \
  -d 'code=authorization-code' \
  -d 'redirect_uri=http://localhost:8000/accounts/amazon-cognito/login/callback/'
