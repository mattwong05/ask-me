import requests


def get_authorization_url(client_id, redirect_uri, scope):
    # 生成跳转到身份提供商(IdP)的授权地址(示例)
    return (
        f"https://example-idp.com/authorize?"
        f"client_id={client_id}&redirect_uri={
            redirect_uri}&scope={scope}&response_type=code"
    )


def exchange_code_for_token(code, client_id, client_secret, redirect_uri):
    # 根据授权码(code)向 IdP 请求令牌(access token 或 ID token)
    resp = requests.post(
        "https://example-idp.com/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri
        }
    )
    return resp.json()


# 示例使用
client_id = "my_client_id"
client_secret = "my_client_secret"
redirect_uri = "https://myapp.com/callback"
scope = "openid profile email"

auth_url = get_authorization_url(client_id, redirect_uri, scope)
print("请将用户引导至该URL完成授权：", auth_url)

# 用户授权后，IdP 回调给我们一个 'code'
# 我们再调用 exchange_code_for_token
code = "example_auth_code"
token_response = exchange_code_for_token(
    code, client_id, client_secret, redirect_uri)
print("拿到的token信息：", token_response)
