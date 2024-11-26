import jwt
from django.contrib.auth import authenticate
from jwt import DecodeError
from jwt.algorithms import RSAAlgorithm
from rest_framework_jwt.settings import api_settings


def get_username_from_payload_handler(payload):
    username = payload.get("sub")
    authenticate(remote_user=username)
    return username


def cognito_jwt_decode_handler(token):
    """
    To verify the signature of an Amazon Cognito JWT, first search for the public key with a key ID that
    matches the key ID in the header of the token. (c)
    https://aws.amazon.com/premiumsupport/knowledge-center/decode-verify-cognito-json-token/
    Almost the same as default 'rest_framework_jwt.utils.jwt_decode_handler', but 'secret_key' feature is skipped
    """
    print("jwt handler", token)
    options = {"verify_exp": api_settings.JWT_VERIFY_EXPIRATION}
    unverified_header = {}
    try:
        unverified_header = jwt.get_unverified_header(token)
    except Exception as e:
        print("Debug exception 1", e)
    if "kid" not in unverified_header:
        print("kid")
        return
        raise DecodeError("Incorrect authentication credentials.")

    kid = unverified_header["kid"]
    print("Try and try")
    try:
        # pick a proper public key according to `kid` from token header
        public_key = RSAAlgorithm.from_jwk(api_settings.JWT_PUBLIC_KEY[kid])
    except KeyError:
        print("KeyError")
        # in this place we could refresh cached jwks and try again
        raise DecodeError("Can't find proper public key in jwks")
    else:
        print(
            "else",
            public_key,
            api_settings.JWT_ALGORITHM,
            # api_settings.JWT_VERIFY,
            "options",options,
            "audience", api_settings.JWT_AUDIENCE,
            "issuer", api_settings.JWT_ISSUER,
            "leeway",api_settings.JWT_LEEWAY,
        )
        decode_text="About"
        print("Token", token)
        try:
            decode_text = jwt.decode(
                token,
                public_key,
                algorithms=[api_settings.JWT_ALGORITHM],
                # api_settings.JWT_VERIFY,
                options=options,
                audience=api_settings.JWT_AUDIENCE,
                issuer=api_settings.JWT_ISSUER,
                leeway=api_settings.JWT_LEEWAY,
            )
        except Exception as e:
            print("Debug exception 2", e)

        print("Decode text", decode_text)
        return jwt.decode(
            token,
            public_key,
            algorithms=[api_settings.JWT_ALGORITHM],
            # api_settings.JWT_VERIFY,
            options=options,
            audience=api_settings.JWT_AUDIENCE,
            issuer=api_settings.JWT_ISSUER,
            leeway=api_settings.JWT_LEEWAY,
        )
