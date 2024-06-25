import requests
import jwt
from jwt.algorithms import RSAAlgorithm
from datetime import datetime

def get_cognito_jwks(region, user_pool_id):
    jwks_url = f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json'
    jwks = requests.get(jwks_url).json()
    return jwks

def validate_token(token, region, user_pool_id, client_id):
    jwks = get_cognito_jwks(region, user_pool_id)
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        print('Client id:', client_id)
        try:
            payload = jwt.decode(
                token,
                RSAAlgorithm.from_jwk(rsa_key),
                algorithms=['RS256'],
                issuer=f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}'
            )
            return payload
        except jwt.ExpiredSignatureError:
            print('Token has expired')
        except jwt.InvalidTokenError as e:
            print(f'Invalid token: {e}')
        except Exception as e:
            print(f'Unable to parse token: {e}')
        return None

# Example usage
token = "eyJraWQiOiJ1cUlHMlNSVDQxSXgrcThPc2VrQlNSMGQ2ZGFJVmNoMkVlRlwvYmNTc3lyND0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyMThiNDVkMC05MGQxLTcwZTUtZTliNC1kMTgwNTI5MTgwM2EiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0yLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMl9pMkVLR0JGRzEiLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiIzNWVoa25wZ2k4dWw4bmZuMnVuZGQ2dWZybyIsImV2ZW50X2lkIjoiOTRkYjI2ZTAtMzUwNS00OGYxLWIxODYtNjcyMjRjNmFiZGU4IiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJvcGVuaWQiLCJhdXRoX3RpbWUiOjE3MTkzMTgzNDYsImV4cCI6MTcxOTMyMTk0NiwiaWF0IjoxNzE5MzE4MzQ2LCJqdGkiOiI4MmMyNTRlNi02OGNlLTQxODQtODEyMS1hZmQ3Zjk3MWRhZjIiLCJ1c2VybmFtZSI6IjIxOGI0NWQwLTkwZDEtNzBlNS1lOWI0LWQxODA1MjkxODAzYSJ9.ERIMl9VHkDzZE6RBddiXXlLNFym_exVjmD_LBerWCZbRk26qpDTmnzDiqi1mOCxvHOHDtw5sLRNOnmOgu6Tl3OF5325jAcZaFIOSCZabDOZb3qhugN-psJ2JHWE3NKZeLRc0MPQUkEPz0_e3KqYghtLs66-vahQidZgn3-vB3bGIKscAC9ZiS6IcajWToehFsuunfjBfehkzgBi-xsJh6tE3jgZW-abQ1d0pzWICGh3ymZhuEcAGJP3L2cIqWxMN0ZhOu9TmuxBFCyk17y7Q6oKlwKXqMeXeWy_jSjXC_-2-Ti6YmZPJL9nahTZ5DpqDn0zSiaSQIPJGitSXVoaxDg"
region = "us-east-2"
user_pool_id = "us-east-2_i2EKGBFG1"
client_id = "35ehknpgi8ul8nfn2undd6ufro"

payload = validate_token(token, region, user_pool_id, client_id)
if payload:
    print("Token is valid")
    print(payload)
else:
    print("Token is invalid")
