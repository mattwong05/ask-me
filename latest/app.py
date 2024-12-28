# 导入必要的模块
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import os

# 创建 Flask 应用实例
app = Flask(__name__)

# 配置应用密钥和数据库路径
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'A_RANDOM_SECRET_KEY'  # 请替换为自己的密钥
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 定义留言模型
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    contact = db.Column(db.String(64))
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    replies = db.relationship('Reply', backref='message', lazy='dynamic')

    def __repr__(self):
        return '<Message %r>' % self.content

# 定义回复模型
class Reply(db.Model):
    __tablename__ = 'replies'
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'))
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Reply %r>' % self.content

# 定义留言表单
class MessageForm(FlaskForm):
    name = StringField('姓名（可选）')
    contact = StringField('联系方式（可选）')
    content = TextAreaField('留言内容', validators=[DataRequired(message="留言内容不能为空")])
    submit = SubmitField('提交')

# 定义回复表单
class ReplyForm(FlaskForm):
    content = TextAreaField('回复内容', validators=[DataRequired(message="回复内容不能为空")])
    submit = SubmitField('回复')

# 主页路由，显示留言列表和留言表单
@app.route('/', methods=['GET', 'POST'])
def index():
    form = MessageForm()
    if form.validate_on_submit():
        # 创建并保存新留言
        message = Message(
            name=form.name.data,
            contact=form.contact.data,
            content=form.content.data
        )
        db.session.add(message)
        db.session.commit()
        flash('留言已提交！', 'success')
        return redirect(url_for('index'))
    # 查询所有留言，按时间倒序排列
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('index.html', form=form, messages=messages)

# 留言详情页路由，显示单个留言和其回复
@app.route('/message/<int:id>', methods=['GET', 'POST'])
def message_detail(id):
    message = Message.query.get_or_404(id)
    form = ReplyForm()
    if form.validate_on_submit():
        # 创建并保存新回复
        reply = Reply(
            content=form.content.data,
            message=message
        )
        db.session.add(reply)
        db.session.commit()
        flash('回复已提交！', 'success')
        return redirect(url_for('message_detail', id=id))
    # 查询该留言的所有回复，按时间正序排列
    replies = message.replies.order_by(Reply.timestamp.asc()).all()
    return render_template('message_detail.html', message=message, form=form, replies=replies)

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)