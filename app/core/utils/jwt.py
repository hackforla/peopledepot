# todo: fix
# get expired to work
import traceback

import jwt
from django.contrib.auth import authenticate
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
    Almost the same as default 'rest_framework_jwt.utils.jwt', but 'secret_key' feature is skipped
    """
    try:
        options = {"verify_exp": api_settings.JWT_VERIFY_EXPIRATION}
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header["kid"]
        # pick a proper public key according to `kid` from token header
        public_key = RSAAlgorithm.from_jwk(api_settings.JWT_PUBLIC_KEY[kid])
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
    except Exception as e:
        print(traceback.format_exc())
        print("Authentication failed", repr(e))
        raise e
