# coding=utf-8

from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from leancloud import Engine
from gevent import monkey


monkey.patch_all()  # 或者只 patch 指定的模块

app = Flask(__name__)
app.config['SECRET_KEY'] = '23438935-0471-11e5-9bcd-34363bd45c90'
Bootstrap(app)

from apps.auth import auth_app

app.register_blueprint(auth_app, url_prefix='/auth')

from apps.sms_task import sms_task_app

app.register_blueprint(sms_task_app, url_prefix='/sms_task')

# LeanEngine 云函数
engine = Engine(app)


@app.route('/')
def index():
    return redirect(url_for('sms_task.index'))