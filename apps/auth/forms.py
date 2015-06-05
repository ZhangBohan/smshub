# coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, validators, SubmitField, PasswordField
__author__ = 'bohan'


class UserForm(Form):
    username = StringField(u'用户名', [validators.DataRequired()])
    email = StringField(u'Email地址', [validators.Email()])
    password = PasswordField(u'密码', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message=u'两次输入的密码必须相同')
    ])
    confirm = PasswordField(u'确认密码')
    submit = SubmitField(u'注册')


class LoginForm(Form):
    username = StringField(u'用户名', [validators.DataRequired()])
    password = PasswordField(u'密码', [validators.DataRequired()])
    submit = SubmitField(u'登录')