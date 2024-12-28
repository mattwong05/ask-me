from flask import Flask, request, render_template, url_for, redirect, flash
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'SIMPLE_SECRET_KEY'
user_dict = {}

def save_user_dict():
    """保存用户数据到文件"""
    with open('user_dict.json', 'w') as f:
        json.dump(user_dict, f)

def load_user_dict():
    """加载用户数据从文件"""
    global user_dict
    if os.path.exists('user_dict.json'):
        with open('user_dict.json', 'r') as f:
            user_dict = json.load(f)

def create_or_update_user_dict(user, welcome):
    """创建或更新用户数据"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 本地时间
    if user not in user_dict:
        # 创建新用户，存储欢迎语和加入时间
        user_dict[user] = {
            "welcome": welcome,
            "join_time": current_time
        }
    else:
        # 更新用户的欢迎语
        user_dict[user]["welcome"] = welcome
    save_user_dict()

def delete_user_dict(user):
    """删除用户数据"""
    if user in user_dict:
        del user_dict[user]
        save_user_dict()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = request.form.get('user', '').strip()
        welcome = request.form.get('welcome', '').strip()

        if not user or not welcome:
            flash("用户名和欢迎消息不能为空！", "error")
            return redirect(url_for('index'))

        status = "创建" if user not in user_dict else "更新"
        create_or_update_user_dict(user, welcome)
        flash(f"{status} 用户 {user} 成功！", "success")
        return redirect(url_for('user_detail', user_name=user))

    return render_template('index-v2.html', user_dict=user_dict)

@app.route('/user/<user_name>')
def user_detail(user_name):
    if user_name not in user_dict:
        flash(f"用户 {user_name} 不存在！", "error")
        return redirect(url_for('index'))

    user_data = user_dict[user_name]
    return render_template('user_detail-v2.html', user_name=user_name, user_data=user_data)

if __name__ == '__main__':
    load_user_dict()
    app.run(port=5210, debug=True)