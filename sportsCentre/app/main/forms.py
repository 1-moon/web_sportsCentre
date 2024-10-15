import sqlite3, hashlib
from flask import *
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField

class searchProd(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])

def parse(data):
	ans = []
	i = 0
	while i < len(data):
		curr = []
		for j in range(7):
			if i >= len(data):
				break
			curr.append(data[i])
			i += 1
		ans.append(curr)
	return ans

def getLoginDetails():
	with sqlite3.connect('app.db') as conn:
		cur = conn.cursor()
		if 'email' not in session:
			loggedIn = False
			firstName = ''
		else:
			loggedIn = True
			cur.execute("SELECT userId, firstName FROM users WHERE email = ?", (session['email'], ))
			firstName = cur.fetchone()
	conn.close()
	return (loggedIn, firstName)


def is_valid(email, password):
	con = sqlite3.connect('app.db')
	cur = con.cursor()
	cur.execute('SELECT email, password FROM users')
	data = cur.fetchall()
	for row in data:
		if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
			return True
	return False

def egetLoginDetails():
	with sqlite3.connect('app.db') as conn:
		cur = conn.cursor()
		if 'email' not in session:
			loggedIn = False
			firstName = ''
		else:
			loggedIn = True
			cur.execute("SELECT userId, firstName FROM eusers WHERE email = ?", (session['email'], ))
			userId, firstName = cur.fetchone()
	conn.close()

	return (loggedIn, firstName)

def eis_valid(email, password):
	con = sqlite3.connect('app.db')
	cur = con.cursor()
	cur.execute('SELECT email, password FROM eusers')
	data = cur.fetchall()
	for row in data:
		if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
			return True
	return False

def mgetLoginDetails():
	with sqlite3.connect('app.db') as conn:
		cur = conn.cursor()
		if 'email' not in session:
			loggedIn = False
			firstName = ''
		else:
			loggedIn = True
			cur.execute("SELECT userId, firstName FROM musers WHERE email = ?", (session['email'], ))
			firstName = cur.fetchone()
	conn.close()

	return (loggedIn, firstName)

def mis_valid(email, password):
	con = sqlite3.connect('app.db')
	cur = con.cursor()
	cur.execute('SELECT email, password FROM musers')
	data = cur.fetchall()
	for row in data:
		if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
			return True
	return False


def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1] in set(['jpeg', 'jpg', 'png', 'gif'])
