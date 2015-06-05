# coding=utf-8
from flask import request, flash, render_template, redirect, url_for, session
from leancloud import User, LeanCloudError

__author__ = 'bohan'

from .forms import UserForm, LoginForm
from . import auth_app


@auth_app.route('/register', methods=['get', 'post'])
def register():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User()
        user.set("username", form.username.data)
        user.set("password", form.password.data)
        user.set("email", form.email.data)

        user.sign_up()
        flash(u'注册成功', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)


@auth_app.route('/login', methods=['get', 'post'])
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
            return redirect(url_for('.index'))
        except LeanCloudError, e:
            flash(e.error, 'danger')

    return render_template('login.html', form=form)