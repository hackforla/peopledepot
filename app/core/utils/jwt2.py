import jwt
from jwt import DecodeError
from jwt.algorithms import RSAAlgorithm
from rest_framework_jwt.settings import api_settings


def get_unverified_header(token):
    return jwt.get_unverified_header(token)


def get_public_key(kid):
    try:
        return RSAAlgorithm.from_jwk(api_settings.JWT_PUBLIC_KEY[kid])
    except KeyError:
        raise DecodeError("Can't find proper public key in jwks")


def decode_token(token, public_key, options):
    try:
        return jwt.decode(
            token,
            public_key,
            algorithms=[api_settings.JWT_ALGORITHM],
            options=options,
            audience=api_settings.JWT_AUDIENCE,
            issuer=api_settings.JWT_ISSUER,
            leeway=api_settings.JWT_LEEWAY,
        )
    except Exception as e:
        raise DecodeError("Can't decode token: " + str(e))


def cognito_jwt_decode_handler(token):
    options = {"verify_exp": api_settings.JWT_VERIFY_EXPIRATION}
    unverified_header = get_unverified_header(token)

    if "kid" not in unverified_header:
        raise DecodeError("Incorrect authentication credentials.")

    kid = unverified_header["kid"]
    public_key = get_public_key(kid)
    decoded = decode_token(token, public_key, options)
    return decoded
