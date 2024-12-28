import hashlib
import os


def hash_password_salted(password, salt=None):
    if not salt:
        salt = os.urandom(16)  # 生成16字节随机盐
    pwd_hash = hashlib.sha256(salt + password.encode()).hexdigest()
    return salt, pwd_hash


users_db_salted = {}


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


# 测试
register_user("alice", "password123")
print(authenticate_salted("alice", "password123"))  # True
