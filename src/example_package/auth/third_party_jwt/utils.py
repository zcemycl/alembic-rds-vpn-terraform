import requests

# https://docs.aws.amazon.com/cognito/latest/developerguide/federation-endpoints.html
URL_CONF = (
    "http://localhost:8002/default_issuer/.well-known/openid-configuration"
)
URL_TOKEN = "http://localhost:8002/default_issuer/token"
URL_JWKS = "http://localhost:8002/default_issuer/jwks"
URL_USERINFO = "http://localhost:8002/default_issuer/userinfo"
URL_REVOKE = "http://localhost:8002/default_issuer/revoke"
URL_END = "http://localhost:8002/default_issuer/.well-known/endsession"
URL_INTROSPECT = "http://localhost:8002/default_issuer/introspect"


"""
Separate Authentication Provider
"""


def get_well_known_endpoint(url: str = URL_CONF):
    resp = requests.get(url).json()
    return resp


# https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html
def get_token(
    grant_type: str = None,
    client_id: str = None,
    client_secret: str = None,
    refresh_token: str = None,
    user: str = None,
    url: str = URL_TOKEN,
):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": grant_type,
        "client_id": client_id,
        "client_secret": client_secret,
        "mock_type": user,
        # "scope": "http://localhost:8002/default_issuer/introspect"
    }
    if grant_type == "refresh_token":
        data["refresh_token"] = refresh_token
    resp = requests.post(
        url,
        headers=headers,
        data=data,
    )
    return resp.json()


# https://docs.aws.amazon.com/cognito/latest/developerguide/userinfo-endpoint.html
def get_user_info(token: str, url: str = URL_USERINFO):
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    return resp.json()


# https://is.docs.wso2.com/en/latest/references/concepts/authentication/jwks/
def get_jwks(url: str = URL_JWKS):
    resp = requests.get(url)
    return resp.json()


# https://docs.aws.amazon.com/cognito/latest/developerguide/revocation-endpoint.html
def revoke_token(
    token: str, token_type: str = "refresh_token", url: str = URL_REVOKE
):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(
        url,
        headers=headers,
        data={
            "client_id": "fake",
            "token": token,
            "token_type_hint": token_type,  # only refresh_token
        },
    )
    print(resp)
    print(resp.text)


# https://www.oauth.com/oauth2-servers/token-introspection-endpoint/
def introspect(token: str, url: str = URL_INTROSPECT):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {token}",
    }
    resp = requests.post(
        url,
        headers=headers,
        data={
            "client_id": "fake",
            "client_secret": "fake",
            "token": token,
            # "token_type_hint": "refresh_token",
        },
    )
    print(resp)
    print(resp.text)


# https://www.npmjs.com/package/oauth2-mock-server?activeTab=readme
def end_session(url: str = URL_END):
    resp = requests.get(url)
    print(resp)
    print(resp.text)


if __name__ == "__main__":
    # print(get_well_known_endpoint())
    # token_resp_user = get_token(
    #     grant_type="client_credentials",
    #     client_id="fake",
    #     client_secret="fake",
    #     user="user",
    # )
    # token_resp_admin = get_token(
    #     grant_type="client_credentials",
    #     client_id="fake",
    #     client_secret="fake",
    #     user="admin",
    # )
    # print("-------Token--------\n ")
    # print(token_resp_user)
    # print(token_resp_admin)
    # print(get_user_info(token_resp_user["access_token"]))
    # print(get_user_info(token_resp_admin["access_token"]))

    # new_token_resp_user = get_token(
    #     grant_type="refresh_token",
    #     client_id="fake",
    #     client_secret="fake",
    #     refresh_token=token_resp_user["access_token"],
    #     user="user",
    # )
    # print(get_user_info(new_token_resp_user["access_token"]))

    # print("------- jwks -------\n")
    # print(get_jwks())
    # introspect(new_token_resp_user["access_token"])
    # revoke_token(new_token_resp_user["access_token"])
    # introspect(new_token_resp_user["access_token"])

    # end_session()
    # introspect(new_token_resp_user["access_token"])
    # introspect(token_resp_admin["access_token"])

    # https://identityserver4.readthedocs.io/en/latest/endpoints/authorize.html#
    auth_resp = requests.get(
        "http://localhost:8002/default_issuer/authorize",
        params={
            "client_id": "fake",
            # "response_type": "id_token token",
            # "scope": "openid profile",
            "response_type": "code",
            "scope": "openid",
            "redirect_uri": "http://localhost:4555/login_page",
            "state": "abc",
            "nonce": "abc",
            # "code": "1234"
        },
        data={"username": "user"},
    )
    print(auth_resp.text)
    print(auth_resp.json())
