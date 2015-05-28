# coding=utf-8
import functools
from flask import Flask, render_template, redirect, url_for, request, flash, session, abort

from flask.ext.wtf import Form
from wtforms import StringField, validators, TextAreaField, SubmitField, PasswordField
from flask_bootstrap import Bootstrap

from leancloud import Object, Query, User, LeanCloudError

from leancloud import Engine

from gevent import monkey

monkey.patch_all()  # 或者只 patch 指定的模块


app = Flask(__name__)
app.config['SECRET_KEY'] = '23438935-0471-11e5-9bcd-34363bd45c90'
Bootstrap(app)

# LeanEngine 云函数
engine = Engine(app)

SmsTask = Object.extend('SmsTask')


def admin_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        if 'user' in session:
            request.user = session.get('user')
            return func(*args, **kw)
        return redirect(url_for('login'))
    return wrapper


class SmsTaskForm(Form):
    name = StringField(u'名称', [validators.DataRequired()])
    mobile = StringField(u'电话', [validators.DataRequired()])
    description = TextAreaField(u'描述')
    effected_at = StringField(u'生效时间')
    submit = SubmitField(u'提交')


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


@app.route('/auth/register', methods=['get', 'post'])
def register():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User()
        user.set("username", form.username.data)
        user.set("password", form.password.data)
        user.set("email", form.email.data)

        user.sign_up()
        flash(u'注册成功', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/auth/login', methods=['get', 'post'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            u = User()
            u.login(form.username.data, form.password.data)
            data = u.attributes
            data['id'] = u.id
            data['updated_at'] = u.updated_at
            data['created_at'] = u.created_at
            session['user'] = u.attributes
            return redirect(url_for('index'))
        except LeanCloudError, e:
            flash(e.error, 'danger')

    return render_template('login.html', form=form)


@app.route('/')
def hello_world():
    return redirect(url_for('index'))


@app.route('/sms_tasks')
@admin_required
def index():
    sms_tasks = Query(SmsTask).equal_to('user_id', request.user.get('id')).find()
    return render_template('list.html', sms_tasks=sms_tasks)


@app.route('/sms_tasks/add', methods=['get'])
@admin_required
def add_get():
    form = SmsTaskForm()
    return render_template('add.html', form=form)


@app.route('/sms_tasks/add', methods=['post'])
@admin_required
def add_post():
    """
    提交数据

    :return:
    """
    form = SmsTaskForm(request.form)
    if not form.validate():
        return render_template('add.html', form=form)
    st = SmsTask()
    st.set('user_id', request.user.get('id'))
    st.set('name', form.name.data)
    st.set('mobile', form.mobile.data)
    st.set('effected_at', form.effected_at.data)
    st.set('description', form.description.data)
    st.set('status', False)
    st.save()
    flash(u'增加成功', 'success')
    return redirect(url_for('index'))


@app.route('/sms_tasks/<task_id>/edit', methods=['get'])
@admin_required
def edit_get(task_id):
    st = Query(SmsTask).equal_to('user_id', request.user.get('id')).get(task_id)
    if not st: abort(404)
    form = SmsTaskForm(**st.attributes)
    return render_template('add.html', form=form)


@app.route('/sms_tasks/<task_id>/edit', methods=['post'])
@admin_required
def edit_post(task_id):
    """
    提交数据

    :return:
    """
    st = Query(SmsTask).equal_to('user_id', request.user.get('id')).get(task_id)
    if not st: abort(404)

    form = SmsTaskForm(request.form)
    if not form.validate():
        return render_template('add.html', form=form)
    st.set('name', form.name.data)
    st.set('mobile', form.mobile.data)
    st.set('effected_at', form.effected_at.data)
    st.set('description', form.description.data)
    st.set('status', False)
    st.save()
    flash(u'修改成功', 'success')
    return redirect(url_for('index'))


@app.route('/sms_tasks/<task_id>/delete')
@admin_required
def delete(task_id):
    st = Query(SmsTask).equal_to('user_id', request.user.get('id')).get(task_id)
    if not st: abort(404)

    st.destroy()
    flash(u'删除成功', 'danger')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
