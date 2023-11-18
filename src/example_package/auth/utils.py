import requests

URL_CONF = (
    "http://localhost:8002/default_issuer/.well-known/openid-configuration"
)
URL_TOKEN = "http://localhost:8002/default_issuer/token"
URL_JWKS = "http://localhost:8002/default_issuer/jwks"
URL_USERINFO = "http://localhost:8002/default_issuer/userinfo"


def get_well_known_endpoint(url: str = URL_CONF):
    resp = requests.get(url).json()
    return resp


def get_token(url: str = URL_TOKEN):
    resp = requests.post(
        url,
        data={
            "grant_type": "client_credentials",
            "client_id": "fake",
            "client_secret": "fake",
            "mock_type": "admin",
        },
    )
    return resp.json()


def get_user_info(token: str, url: str = URL_USERINFO):
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    return resp.json()


def get_jwks(url: str = URL_JWKS):
    resp = requests.get(url)
    return resp.json()


if __name__ == "__main__":
    print(get_well_known_endpoint())
    token_resp = get_token()
    print(token_resp)
    print(get_jwks())
    print(get_user_info(token_resp["access_token"]))
