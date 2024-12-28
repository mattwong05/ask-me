import hashlib

PEPPER = "SuperSecretPepperValue"


def hash_password_pepper(password):
    combined = password + PEPPER
    return hashlib.sha256(combined.encode()).hexdigest()


# 示意写法，与版本2类似
users_db_pepper = {
    "alice": hash_password_pepper("password123")
}


def authenticate_pepper(username, password):
    if username not in users_db_pepper:
        return False
    return users_db_pepper[username] == hash_password_pepper(password)
