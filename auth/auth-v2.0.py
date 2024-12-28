import hashlib

# 版本2：单向哈希


def simple_hash_password(password) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


users_db_hash = {
    "alice": hash_password("password123"),
    "bob": hash_password("qwerty")
}


def authenticate_hash(username, password):
    if username in users_db_hash:
        return users_db_hash[username] == hash_password(password)
    return False


# 测试
print(authenticate_hash("alice", "password123"))  # True
