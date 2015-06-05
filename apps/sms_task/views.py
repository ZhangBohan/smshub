# coding=utf-8
from flask import request, flash, render_template, redirect, url_for, abort
from leancloud import Query
from services.utils import admin_required

__author__ = 'bohan'

from .forms import SmsTaskForm
from .models import SmsTask
from . import sms_task_app


@sms_task_app.route('/')
@admin_required
def index():
    sms_tasks = Query(SmsTask).equal_to('user_id', request.user.get('id')).find()
    return render_template('list.html', sms_tasks=sms_tasks)


@sms_task_app.route('/add', methods=['get'])
@admin_required
def add_get():
    form = SmsTaskForm()
    return render_template('add.html', form=form)


@sms_task_app.route('/add', methods=['post'])
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


@sms_task_app.route('/<task_id>/edit', methods=['get'])
@admin_required
def edit_get(task_id):
    st = Query(SmsTask).equal_to('user_id', request.user.get('id')).get(task_id)
    if not st: abort(404)
    form = SmsTaskForm(**st.attributes)
    return render_template('add.html', form=form)


@sms_task_app.route('/<task_id>/edit', methods=['post'])
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


@sms_task_app.route('/<task_id>/delete')
@admin_required
def delete(task_id):
    st = Query(SmsTask).equal_to('user_id', request.user.get('id')).get(task_id)
    if not st: abort(404)

    st.destroy()
    flash(u'删除成功', 'danger')
    return redirect(url_for('index'))
