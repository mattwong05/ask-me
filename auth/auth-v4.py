import secrets
import os
import hashlib

sessions = {}  # session_id -> username
users_db_salted = {}


def hash_password_salted(password, salt=None):
    if not salt:
        salt = os.urandom(16)  # 生成16字节随机盐
    pwd_hash = hashlib.sha256(salt + password.encode()).hexdigest()
    return salt, pwd_hash


def register_user(username, password):
    salt, pwd_hash = hash_password_salted(password)
    users_db_salted[username] = {
        "salt": salt,
        "hash": pwd_hash
    }


def authenticate_salted(username, password):
    user_data = users_db_salted.get(username)
    if not user_data:
        return False
    salt = user_data["salt"]
    stored_hash = user_data["hash"]
    _, pwd_hash = hash_password_salted(password, salt)
    return pwd_hash == stored_hash


def login_session(username, password):
    # 这里可复用前面加盐哈希逻辑，这里简化处理
    user_data = users_db_salted.get(username)
    if not user_data:
        return None

    salt = user_data["salt"]
    stored_hash = user_data["hash"]
    _, pwd_hash = hash_password_salted(password, salt)

    if pwd_hash == stored_hash:
        session_id = secrets.token_hex(16)
        sessions[session_id] = username
        return session_id
    else:
        return None


def authenticate_session(session_id):
    return sessions.get(session_id, None)


# 测试
sid = login_session("alice", "password123")
print("Alice的 session ID:", sid)
print("通过 session 认证获取的用户名:", authenticate_session(sid))
