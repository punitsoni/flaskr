import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
import platform
import psutil

from app import app
from app import sys_info

@app.route('/old')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
        g.db.execute('insert into entries (title, text) values (?, ?)',
           [request.form['title'], request.form['text']])
        g.db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were successfully logged out.')
    return redirect(url_for('home'))

@app.route('/')
@app.route('/home')
def home():
    posts=[]
    cur = g.db.execute('select title, text from entries order by id desc')
    posts = [dict(name=row[0], message=row[1]) for row in cur.fetchall()]
    return render_template("home.html", posts=posts)

@app.route('/addpost', methods=['POST'])
def add_post():
    g.db.execute('insert into entries (title, text) values (?, ?)', \
        [request.form['name'], request.form['message']])
    g.db.commit()
    flash('Your message was successfully posted.')
    return redirect(url_for('home'))

@app.route('/sysinfo')
def sysinfo():
    sys_info['mem_usage'] = psutil.virtual_memory()
    sys_info['cpu_util'] = psutil.cpu_percent(percpu=True, interval=None)
    return render_template('sysinfo.html', sys_info=sys_info)

@app.route('/ajax/sysinfo')
def ajax_sysinfo():
    sys_info['mem_usage_percent'] = psutil.virtual_memory().percent
    sys_info['mem_total'] = psutil.virtual_memory().total
    sys_info['mem_used'] = psutil.virtual_memory().used
    sys_info['cpu_util'] = psutil.cpu_percent(percpu=True, interval=None)
    #data = jsonify(results=["1", "2", "3"], name="Punit")
    return jsonify(sysinfo=sys_info)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = "Invalid username"
        elif request.form['password'] != app.config['PASSWORD']:
            error = "Invalid passowrd"
        else:
            session['logged_in'] = True
            flash('You are logged in.')
    return render_template('admin.html', error=error)

@app.route('/del_posts', methods=['POST'])
def del_posts():
    print "deleting all posts"
    g.db.execute('delete from entries')
    g.db.commit()
    return "success"
