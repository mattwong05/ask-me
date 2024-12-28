from flask import Flask, request, render_template_string, url_for
import os
import datetime
import json


app = Flask(__name__)

user_dict = {
    'Cross': ["Hello，I'm Cross!", "2024-11-23", ["message1", "message2", "message3"]],
    'Matt': ["Nice to meet you!", "2024-11-30"],
}


user_dict = {
    'Cross': {
        'welcome': "Hello，I'm Cross!",
        'create_date': "2024-11-23",
        'messages': [
            {
                "theme": "My first Post",
                "reply": [
                    "Well done!",
                    "Good job!",
                    "🏴‍☠️"
                    ],
            },
            {
                "theme": "My second Post",
                "reply": [
                    "Good job!",
                    "Well done!",
                    ],
            }
        ]
    },
    'Matt': {
        'welcome': "Nice to meet you!",
        'create_date': "2024-11-30",
        'messages': []
    }
}

def save_user_dict():
    with open('user_dict_v1.txt', 'w') as f:
        for user_name, user_data in user_dict.items():
            f.write(f'{user_name},{user_data[0]},{user_data[1]}\n')

def load_user_dict():
    # 如果文件不存在，则创建一个空文件
    if not os.path.exists('user_dict_v1.txt'):
        with open('user_dict_v1.txt', 'w') as f:
            pass  # 创建空文件

    # 加载文件内容到字典
    with open('user_dict_v1.txt', 'r') as f:
        for line in f:
            values = line.strip().split(',')
            print(values)
            user_dict[values[0]] = [values[1], values[2]]

def create_or_update_user_dict(user, welcome):
    user_dict[user] = [welcome, datetime.datetime.now().strftime(r'%Y-%m-%d')]
    save_user_dict()

def delete_user_dict(user):
    del user_dict[user]
    save_user_dict()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = request.form['user']
        welcome = request.form['welcome']
        status = "创建" if user not in user_dict else "更新"
        # TODO: 检验用户输入是否不为空
        create_or_update_user_dict(user, welcome)
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>操作成功</title>
            </head>
            <body>
                <h1>{{ status }} 用户 {{ user }} 成功！</h1>
                <p>欢迎消息：{{ welcome }}</p>
                <a href="{{ url_for('index') }}">返回首页</a>
                <a href="/user/{{ user }}">查看用户</a>
            </body>
            </html>                           
                                      ''', status=status, user=user, welcome=welcome)
    
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>创建用户</title>
        </head>
        <body>
            <h1>创建或更新用户</h1>
            <form method="POST">
                用户名：<input type="text" name="user"><br>
                欢迎消息：<input type="text" name="welcome"><br>
                <button type="submit">提交</button>
            </form>
            <h2>现有用户</h2>
            <ul>
                {% for user, welcome in user_dict.items() %}
                <li><a href="/user/{{ user }}">{{ user }}: {{ welcome }}</a></li>
                {% endfor %}
            </ul>
        </body>
        </html>
    ''', user_dict=user_dict)


# 定义动态路由
@app.route('/user/<user_name>')
def user_question_box(user_name):
    if user_name not in user_dict:
        return f'用户 {user_name} 不存在！<br><a href="/">返回主页面</a>'
    return f'{user_dict[user_name]}<br><a href="/">返回主页面</a>'


if __name__ == '__main__':
    load_user_dict()
    app.run(port=5210, debug=True)
