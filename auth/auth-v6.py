import secrets


def generate_otp_secret():
    return secrets.token_hex(8)  # 生成一次性验证的秘钥或种子


def verify_otp(otp_secret, user_input_code):
    # 这里仅作示例，可使用 pyotp 等库生成/校验 TOTP
    return user_input_code == "123456"  # 假设 "123456" 是正确码


def login_mfa(username, password, otp_code, otp_secret):
    # 示例：先进行密码验证（可复用之前盐哈希逻辑）
    user_data = users_db_salted.get(username, None)
    if not user_data:
        return None

    salt = user_data["salt"]
    stored_hash = user_data["hash"]
    _, pwd_hash = hash_password_salted(password, salt)
    if pwd_hash != stored_hash:
        return None

    # 再进行一次性验证码验证
    if not verify_otp(otp_secret, otp_code):
        return None

    # 如果都通过，就返回某种会话或令牌
    return "MFA_SUCCESS_TOKEN"


# 测试
user_otp_secret = generate_otp_secret()
result = login_mfa("alice", "password123", "123456", user_otp_secret)
print("MFA 认证结果：", result)
