import hashlib

# 明文词典（模拟常用密码）
plaintext_passwords = ["password123", "123456", "qwerty", "admin", "letmein"]

# 生成 MD5 彩虹表


def generate_rainbow_table(plaintexts):
    table = {}
    for plaintext in plaintexts:
        hashed = hashlib.md5(plaintext.encode()).hexdigest()
        table[plaintext] = hashed
    return table

# 演示彩虹表破解


def demonstrate_rainbow_attack(hash_value, rainbow_table):
    for plaintext, hashed in rainbow_table.items():
        if hashed == hash_value:
            return f"破解成功！明文为: {plaintext}"
    return "破解失败: 不在彩虹表中"


# 生成彩虹表并测试
rainbow_table = generate_rainbow_table(plaintext_passwords)
test_hash = hashlib.md5("password123".encode()).hexdigest()  # 对应 "password123"
print("测试彩虹表攻击...")
print(demonstrate_rainbow_attack(test_hash, rainbow_table))
