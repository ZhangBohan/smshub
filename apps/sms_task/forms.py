# coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, validators, SubmitField, TextAreaField
__author__ = 'bohan'


class SmsTaskForm(Form):
    name = StringField(u'名称', [validators.DataRequired()])
    mobile = StringField(u'电话', [validators.DataRequired()])
    description = TextAreaField(u'描述')
    effected_at = StringField(u'生效时间')
    submit = SubmitField(u'提交')