import time

users_db = {
    "alice": "password123"
}

failed_attempts = {}  # 记录某一username的失败次数
lockout_until = {}    # 记录某一username被锁定到何时

MAX_ATTEMPTS = 3
COOLDOWN_TIME = 30  # 30秒


def authenticate_cooldown(username, password):
    current_time = time.time()
    # 如果已被锁定且时间未到，则直接返回False
    if username in lockout_until and current_time < lockout_until[username]:
        return False

    if username in users_db and users_db[username] == password:
        failed_attempts[username] = 0  # 重置失败次数
        return True
    else:
        failed_attempts[username] = failed_attempts.get(username, 0) + 1
        if failed_attempts[username] >= MAX_ATTEMPTS:
            lockout_until[username] = current_time + COOLDOWN_TIME
        return False


# 测试
for i in range(4):
    print(authenticate_cooldown("alice", "wrong"))  # 第3次后锁定
