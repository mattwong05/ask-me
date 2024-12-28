# Version 1: 纯文本存储
users_db = {
    "alice": "password123",  # 不安全: 明文存储
    "bob": "qwerty"
}


def authenticate(username, password):
    if username in users_db:
        return users_db[username] == password
    return False


# 测试
print(authenticate("alice", "password123"))  # True
print(authenticate("alice", "wrong"))        # False
