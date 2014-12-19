import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
abort, render_template, flash
from contextlib import closing
import platform
from datetime import timedelta
# import default config module
import flaskr_config

def get_sys_info():
    sys_info = {}
    sys_info['system'] = ('Operating System', platform.system())
    sys_info['processor'] = ('Microprocessor', platform.processor())
    sys_info['architecture'] = ('Architecture', platform.architecture())
    sys_info['node'] = ('Host name', platform.node())
    return sys_info

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
            db.commit()
    return app.config['DATABASE']

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


# module init code
app = Flask(__name__)
app.config.from_object(flaskr_config)
app.config.from_envvar('FLASKR_CONFIG', silent=True)
sys_info = get_sys_info()

@app.before_request
def before_request():
    g.db = connect_db()
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

from app import views