#!/bin/bash
source ../../venv/bin/activate
source ../../../scripts/loadenv.sh .env.local
# Check if the correct number of parameters is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <username> <password> <json_string>"
    return 1
fi

# Assign parameters to variables
first_name=$1
password=$2
json_string=$3
username=$first_name

# Get the token and user id
echo Getting token
ENCRYPTED_password=$(echo -n "$password" | base64)
echo Encrypted password: $ENCRYPTED_password
TOKEN_RESPONSE=$(curl -v -X POST http://localhost:8000/api/v1/api/token/ -H "Content-Type: application/json" -d '{"username": "'"$username"'", "password": "'"$password"'"}')
echo $TOKEN_RESPONSE
# Extract the token and user id from the response

# $1 is the part before "token":" .  $2 is the part after "token":"
string_after_token_label=$(echo "$TOKEN_RESPONSE" | awk -F'"token":' '{print $2}' )

# splits text by " and takes the word after the first ".  $1 is the part before " and $2 is the part before the first ".
token=$(echo "$string_after_token_label" | awk -F'"' '{print $2}')

echo Token $token
echo 

# Check if the token or user_id is empty
if [ -z "$token" ]; then
    echo "Failed to get token or user id"
    return 1
fi

# Make the PATCH request to update the user and capture the response and status code
RESPONSE=$(curl -L -s -o -v response.txt -w "%{http_code}" -X GET "http://localhost:8000/api/v1/users" -H "Content-Type: application/json" -H "Authorization: Bearer $token")
# RESPONSE=$(curl -L -s -o -v response.txt -w "%{http_code}" -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/users/")

# Print the response status code
echo "Status Code: $RESPONSE"

# Print the response body
echo "Response Body:"
cat response.txt

# Clean up the temporary response file
rm response.txt
