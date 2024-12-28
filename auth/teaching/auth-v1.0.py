from typing import Tuple
import time
import hashlib
import os
import uuid

PEPPER = "YOUSEMINAR_yihan1103_ian_zhao_1145141919810_my_youseminar_wangjvnhao_matt_cross_sans_undertale_minecraft_plantvszombies_zh_chinese_china_hu_110114_2011_0817_342224_mycode_mooo_cooo_jidaowansui_JiaoyAnmA1989_fdy_yuanshenqidong_miku"

plaintext_passwords = [
    "password",
    "Password@123",
    "0001",
    "1103",
]

rainbow_table = {}

users_db = {
    "cross": "im_gonecross_youseminar_yihan1103_ian_zhao_1145141919810_my_youseminar_wangjvnhao_matt_cross_sans_undertale_minecraft_plantvszombies_zh_chinese_china_hu_110114_2011_0817_342224_mycode_mooo_cooo_jidaowansui_JiaoyAnmA1989_fdy_yuanshenqidong_miku",
    "matt": "password",
    "manli": "Password@123",
    "yihan": "yihan1103",
    "lock": "1103",
}

users_db_hashed = {
    "cross": "2d273f1b880708e305677fecba215eae",
    "matt": "a086172a3e64807419184757fa06543a",
    "manli": "d033b848d5e61ba89c95c285d346031e",
    "yihan": "fe68ed2c43796c51615f2d62a8a2b553",
    "lock": "a16b53cf32bc8d5136b3770601569aff",
}

# username: (hashed_password, salt)
users_db_hashed_with_salt = {
    "cross": {"hashed": "3539bcc28a8ec90909e3a0880691b013", "salt": "456db7d686f5b8f1b0a91c8b2c010778"},
    "matt": {"hashed": "cfc3e4efd74aba07bbd71cdef286b8ac", "salt": "bf91ba25312340de0ab8b2d969f87a90"},
    "manli": {"hashed": "5cf14dd0165bcd75daa5dda692e0ac0c", "salt": "6bef5ae254d42cf5a116f334e32960f6"},
    "yihan": {"hashed": "8d77f91279f3f979910d6a20f6db4e0a", "salt": "e9bc95a733f22ae51af272bf317a49f3"},
    "lock": {"hashed": "fe7f1b1bd1834f5b7f6a42c28d773e14", "salt": "841441b2977db06de9e99492ef502a02"},
}

BASE_LOCK_TIME_SECONDS = 0.1

fail_attempts = {
    "cross": {
        "attempts": 0,
        "last_attempt": None,
        "locked_until": None,
        "lock_time_seconds": 60,
    }
}


sessions = {
    "session_id": {
        "username": "username",
        "expire_time": time.time(),
    }
}


def simple_hash_password(password: str, salt: str | None = None) -> Tuple[str, str]:
    if not salt:
        salt = os.urandom(16).hex()
    combined = salt + password + PEPPER
    return salt, hashlib.md5(combined.encode()).hexdigest()


def authenticate(username, password) -> Tuple[bool, str]:
    if username not in users_db_hashed:
        return False, "User not found"
    if username not in fail_attempts:
        fail_attempts[username] = {
            "attempts": 0,
            "last_attempt": None,
            "locked_until": None,
            "lock_time_seconds": BASE_LOCK_TIME_SECONDS,
        }
    if fail_attempts[username]["locked_until"] is not None and time.time() < fail_attempts[username]["locked_until"]:
        return False, f"Account locked, try again in {fail_attempts[username]['locked_until'] - time.time()} seconds"
    user_salt = users_db_hashed_with_salt[username]['salt']
    if users_db_hashed_with_salt[username]['hashed'] == simple_hash_password(password, user_salt)[1]:
        fail_attempts[username]["attempts"] = 0
        fail_attempts[username]["last_attempt"] = None
        fail_attempts[username]["locked_until"] = None
        fail_attempts[username]["lock_time_seconds"] = BASE_LOCK_TIME_SECONDS
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "username": username,
            "expire_time": time.time() + 60,
        }
        return True, f"Authentication successful, session_id: {session_id}"
    fail_attempts[username]["attempts"] += 1
    fail_attempts[username]["last_attempt"] = time.time()
    fail_attempts[username]["locked_until"] = time.time(
    ) + fail_attempts[username]["lock_time_seconds"]
    fail_attempts[username]["lock_time_seconds"] *= 2
    return False, "Wrong password"


def authenticate_with_session(session_id) -> Tuple[bool, str]:
    print(sessions)
    if session_id not in sessions:
        return False, "Session not found"
    if sessions[session_id]["expire_time"] < time.time():
        return False, "Session expired"
    return True, f"Authentication successful, username: {sessions[session_id]['username']}"


def generate_rainbow_table():
    for password in plaintext_passwords:
        rainbow_table[simple_hash_password(password)] = password
        print(f"\"{simple_hash_password(password)}\": \"{password}\",")


def login():
    while True:
        print("Welcome to the login system")
        print("1. Login with password")
        print("2. Login with session")
        print("0. Exit")
        input_option = input("Enter option: ")
        if input_option == "1":
            login_with_password()
        elif input_option == "2":
            login_with_session()
        elif input_option == "0":
            break
        else:
            print("Invalid option, please try again")


def login_with_password():
    username = input("Enter username: ")
    password = input("Enter password: ")
    result, message = authenticate(username, password)
    print(message)


def login_with_session():
    session_id = input("Enter session_id: ")
    result, message = authenticate_with_session(session_id)
    print(message)


def brute_force():
    for i in range(10000):
        result, message = authenticate("lock", str(i))
        if result:
            print(f"Success: {message}, password: {i}")
            break

    print(f"Failed: {message}")


def create_hashed_passwords():
    for user in users_db:
        users_db_hashed[user] = simple_hash_password(users_db[user])
        print(f"\"{user}\": \"{users_db_hashed[user]}\",")


def create_hashed_passwords_with_salt():
    for user in users_db:
        salt, hashed = simple_hash_password(users_db[user])
        users_db_hashed_with_salt[user] = (hashed, salt)
        print(f"\"{user}\": {{\"hashed\": \"{hashed}\", \"salt\": \"{salt}\"}},")


if __name__ == "__main__":
    login()

    # create_hashed_passwords_with_salt()

    # print(simple_hash_password("Password@123"))
    # print(simple_hash_password("Password@123"))
