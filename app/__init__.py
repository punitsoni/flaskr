import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
abort, render_template, flash
from contextlib import closing
import platform

# import default config module
import flaskr_config

app = Flask(__name__)
app.config.from_object(flaskr_config)
app.config.from_envvar('FLASKR_CONFIG', silent=True)

sys_info = {}
sys_info['system'] = platform.system()
sys_info['processor'] = platform.processor()
sys_info['architecture'] = platform.architecture()

from app import views

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
            db.commit()
    return app.config['DATABASE']

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()