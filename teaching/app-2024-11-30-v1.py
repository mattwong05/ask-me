from flask import Flask, request, render_template, url_for, redirect, flash
import os

app = Flask(__name__)
app.secret_key = 'SIMPLE_SECRET_KEY'  # 用于闪存消息
user_dict = {}

def save_user_dict():
    """保存用户数据到文件"""
    with open('user_dict.txt', 'w') as f:
        for k, v in user_dict.items():
            f.write(f'{k},{v}\n')

def load_user_dict():
    """加载用户数据从文件"""
    if not os.path.exists('user_dict.txt'):
        open('user_dict.txt', 'w').close()  # 创建空文件

    with open('user_dict.txt', 'r') as f:
        for line in f:
            if ',' in line:
                k, v = line.strip().split(',', 1)
                user_dict[k] = v

def create_or_update_user_dict(user, welcome):
    """创建或更新用户数据"""
    user_dict[user] = welcome
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

    return render_template('index.html', user_dict=user_dict)

@app.route('/user/<user_name>')
def user_detail(user_name):
    if user_name not in user_dict:
        flash(f"用户 {user_name} 不存在！", "error")
        return redirect(url_for('index'))

    return render_template('user_detail.html', user_name=user_name, welcome_message=user_dict[user_name])

if __name__ == '__main__':
    load_user_dict()
    app.run(port=5210, debug=True)