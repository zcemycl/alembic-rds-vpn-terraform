import requests

# https://docs.aws.amazon.com/cognito/latest/developerguide/federation-endpoints.html
URL_CONF = (
    "http://localhost:8002/default_issuer/.well-known/openid-configuration"
)
URL_TOKEN = "http://localhost:8002/default_issuer/token"
URL_JWKS = "http://localhost:8002/default_issuer/jwks"
URL_USERINFO = "http://localhost:8002/default_issuer/userinfo"


def get_well_known_endpoint(url: str = URL_CONF):
    resp = requests.get(url).json()
    return resp


def get_token(user: str, url: str = URL_TOKEN):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(
        url,
        headers=headers,
        data={
            "grant_type": "client_credentials",
            "client_id": "fake",
            "client_secret": "fake",
            "mock_type": user,
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
    token_resp_user = get_token("user")
    token_resp_admin = get_token("admin")
    print("-------Token--------\n ")
    print(token_resp_user)
    print(token_resp_admin)
    # print(get_jwks())
    print(get_user_info(token_resp_user["access_token"]))
    print(get_user_info(token_resp_admin["access_token"]))
