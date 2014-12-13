import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import psi
from app import app

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
    return render_template('login.html', error=error)

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
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['name'], request.form['message']])
    g.db.commit()
    flash('Your message was successfully posted.')
    return redirect(url_for('home'))

@app.route('/sysinfo')
def sysinfo():
	entries = {}
	entries['load'] = psi.loadavg()
	return render_template('sysinfo.html', entries=entries)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	error = None
	if request.method == 'POST':
		print "post request"
		if request.form['username'] != app.config['USERNAME']:
			error = "Invalid username"
		elif request.form['password'] != app.config['PASSWORD']:
			error = "Invalid passowrd"
		else:
			session['logged_in'] = True
			flash('You are logged in.')
	print "error: ", error
	return render_template('admin.html', error=error)

@app.route('/del_posts', methods=['POST'])
def del_posts():
	print "deleting all posts"
	g.db.execute('delete from entries')
	g.db.commit()
	return "success"
