from typing import List

from pydantic import BaseModel


# https://stackoverflow.com/questions/60538047/jwt-private-public-key-confusion
# https://openid.net/specs/draft-jones-json-web-key-03.html
# https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-key-set-properties
class JsonWebKey(BaseModel):
    alg: str  # specific cryptographic algorithm
    kty: str  # family of cryptographic algorithms
    use: str  # the intended use of the key. (signature / encryption)
    kid: str  # key id members
    e: str  # exponent for RSA public key
    n: str  # exponent for RSA public key


# https://github.com/navikt/mock-oauth2-server
# https://openid.net/specs/openid-connect-discovery-1_0.html
# https://docs.aws.amazon.com/cognito/latest/developerguide/federation-endpoints.html
class OpenIDConfiguration(BaseModel):
    issuer: str
    authorization_endpoint: str
    end_session_endpoint: str
    revocation_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    jwks_uri: str
    introspection_endpoint: str
    response_types_supported: List[str]
    subject_types_supported: List[str]
    id_token_signing_alg_values_supported: List[str]
    code_challenge_methods_supported: List[str]


# https://pyjwt.readthedocs.io/en/stable/usage.html
class RegisteredClaim(BaseModel):
    exp: int  # Expiration Time
    nbf: int  # Not Before Time
    iss: str  # Issuer
    aud: List[str]  # Audience : the recipients that the JWT is intended for
    iat: int  # Issued At


class StandardClaim(RegisteredClaim):
    sub: str
    name: str
    given_name: str
    family_name: str
    jti: str
    email: str
    preferred_username: str
    phone_number: str
