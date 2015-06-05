import functools
from flask import session, request, redirect, url_for

__author__ = 'bohan'


def admin_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        if 'user' in session:
            request.user = session.get('user')
            return func(*args, **kw)
        return redirect(url_for('auth.login'))

    return wrapper