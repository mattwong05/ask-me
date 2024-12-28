import jwt
import datetime

SECRET_KEY = "mysecret"


def create_jwt(username):
    payload = {
        "user": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # 30分钟后过期
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verify_jwt(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["user"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# 测试
token = create_jwt("alice")
print("Alice的JWT:", token)
print("认证结果:", verify_jwt(token))
