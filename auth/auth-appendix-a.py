import hashlib
import random

# 随机生成一个字符串


def random_string(length=8):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=length))

# 模拟碰撞攻击


def find_collision():
    hash_table = {}
    while True:
        input_data = random_string()  # 生成随机输入
        hash_value = hashlib.md5(input_data.encode()).hexdigest()  # 计算 MD5 哈希

        # 检查是否已经存在相同的哈希值，但输入不同
        if hash_value in hash_table and hash_table[hash_value] != input_data:
            print(f"碰撞找到！")
            print(f"输入1: {hash_table[hash_value]}")  # 之前存储的输入
            print(f"输入2: {input_data}")  # 当前生成的输入
            print(f"相同哈希值: {hash_value}")
            break

        # 如果没有碰撞，将哈希值和对应输入存入表中
        hash_table[hash_value] = input_data


# 测试代码
find_collision()
