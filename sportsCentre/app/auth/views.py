"""
      A file to compose page for authentication
"""
from . import auth
from flask import *
from .forms import parse, searchProd, getLoginDetails, is_valid, mgetLoginDetails, mis_valid, egetLoginDetails, eis_valid
from flask import render_template, redirect, url_for, session
from flask.globals import request
import sqlite3, hashlib, os
import logging
from werkzeug.utils import secure_filename  #for admin


@auth.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('auth.root'))
    else:
        return render_template('auth/login.html')

@auth.route("/")
def root():
    # loggedIn, firstName, noOfItems = getLoginDetails()
    loggedIn, firstName = getLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        # cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        itemData = cur.fetchall()
        # cur.execute('SELECT categoryId, name FROM categories')
        categoryData = cur.fetchall()
    itemData = parse(itemData)
    # app.logger.info('index route request')
    return render_template('index.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, categoryData=categoryData)
    # return render_template('index.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryData=categoryData)

@auth.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):

            session['email'] = email
            return redirect(url_for('auth.root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('auth/login.html', error=error)

@auth.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('auth.root'))

# ================== Manager login area ===========================
@auth.route("/mlogin", methods = ['POST', 'GET'])
def mlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if mis_valid(email, password):

            session['email'] = email
            return redirect(url_for('main.managerhome'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('auth/mlogin.html', error=error)

@auth.route("/mloginForm")
def mloginForm():
    if 'email' in session:
        return redirect(url_for('main.managerhome'))
    else:
        return render_template('auth/mlogin.html')

@auth.route("/mlogout")
def mlogout():
    session.pop('email', None)
    return redirect(url_for('auth.root'))


# ================== Manager Sign up area ===========================
@auth.route("/msignupForm")
def msignupForm():
    return render_template("auth/msignup.html")

@auth.route("/msignup", methods = ['GET', 'POST'])
def msignup():
    if request.method == 'POST':
        #Parse form data
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
       # Check password length
        if len(password) < 8:
            error = 'Password must be at least 8 characters long.'
            return render_template('auth/msignup.html', error=error)

        with sqlite3.connect('app.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO musers (password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, address1, address2, zipcode, city, state, country, phone))

                con.commit()

                msg = "Registered Successfully"
    
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("auth/mlogin.html", error=msg)
    else:
        return render_template("auth/msignup.html")

      

# ================== Employee login area ===========================
@auth.route("/elogin", methods = ['POST', 'GET'])
def elogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if eis_valid(email, password):

            session['email'] = email
            return redirect(url_for('main.employeehome'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('auth/elogin.html', error=error)

@auth.route("/eloginForm")
def eloginForm():
    if 'email' in session:
        return redirect(url_for('main.employeehome'))
    else:
        return render_template('auth/elogin.html')

@auth.route("/elogout")
def elogout():
    session.pop('email', None)
    return redirect(url_for('auth.root'))



# ================== Employee Sign up area ===========================
@auth.route("/esignupForm")
def esignupForm():
    return render_template("auth/esignup.html")
@auth.route("/esignup", methods = ['GET', 'POST'])
def esignup():
    if request.method == 'POST':
        #Parse form data
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        position = request.form['position']
       # Check password length
        if len(password) < 8:
            error = 'Password must be at least 8 characters long.'
            return render_template('auth/esignup.html', error=error)

        with sqlite3.connect('app.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO eusers (password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone, position) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, address1, address2, zipcode, city, state, country, phone, position))

                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()

        return render_template("managerhome.html", error=msg)
    else:
        return render_template("auth/esignup.html")

      
# ================== manager - delete staff ===========================
#by ayesha
@auth.route('/Delete', methods=['GET','POST'])
def Delete():
    if 'email' not in session:
        return render_template('managerhome.html')
    loggedIn, firstName = mgetLoginDetails()
    if request.method == "POST":
          with sqlite3.connect('app.db') as con:
            cur = con.cursor()
            cur.execute('DELETE from eusers ')
            con.commit() 
            return redirect("/staffmembers")
    return render_template("managerhome.html", loggedIn=loggedIn, firstName=firstName)


# ================== Sign up area ===========================
@auth.route("/signupForm")
def signupForm():
    return render_template("auth/signup.html")

@auth.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        #Parse form data
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
       # Check password length
        if len(password) < 8:
            error = 'Password must be at least 8 characters long.'
            return render_template('auth/signup.html', error=error)

        with sqlite3.connect('app.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, address1, address2, zipcode, city, state, country, phone))

                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("index.html", error=msg)
    else:
        return render_template("auth/signup.html")

# ============================== cookie area===============
@auth.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
    loggedIn, firstName = getLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM facility')
        itemData = cur.fetchall()
        if loggedIn == True:
            cur.execute("SELECT userId, firstName FROM users WHERE email = ?", (session['email'],))
            userId = cur.fetchone()[0]
        else:
            userId = None
    itemData = parse(itemData)

    global resp
    if request.method == 'POST':
        resp = make_response(render_template('index.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName))
        if loggedIn == True:
            resp.set_cookie('user_id', str(userId))
            return resp
        else:
            resp.set_cookie('user_id', str(userId), max_age=0)
            return resp
    else:
        return render_template('home.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName)

@auth.route('/getcookie')
def getcookie():
   name = request.cookies.get('user_id')
   return (f"<h1 style=\"text-align: center\">Cookie value set to: {name}</h1><a style=\"background-color: skyblue; color: black; margin-left: 800px; padding: 0px 10px 0px 10px; border-radius: 5px; text-decoration: none\" href=\"/\">Go To Your Home</a>")

# ============================== Manager cookie area ===============
@auth.route('/msetcookie', methods = ['POST', 'GET'])
def msetcookie():
    loggedIn, firstName = mgetLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM facility')
        itemData = cur.fetchall()
        if loggedIn == True:
            cur.execute("SELECT userId, firstName FROM musers WHERE email = ?", (session['email'],))
            userId = cur.fetchone()[0]
        else:
            userId = None
    itemData = parse(itemData)

    global resp
    if request.method == 'POST':
        resp = make_response(render_template('managerhome.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName))
        if loggedIn == True:
            resp.set_cookie('user_id', str(userId))
            return resp
        else:
            resp.set_cookie('user_id', str(userId), max_age=0)
            return resp
    else:
        return render_template('managerhome.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName)

@auth.route('/mgetcookie')
def mgetcookie():
   name = request.cookies.get('user_id')
   return (f"<h1 style=\"text-align: center\">Cookie value set to: {name}</h1><a style=\"background-color: skyblue; color: black; margin-left: 800px; padding: 0px 10px 0px 10px; border-radius: 5px; text-decoration: none\" href=\"/managerhome\">Go To Manager Home</a>")


# ============================== Employee cookie area ===============
@auth.route('/esetcookie', methods = ['POST', 'GET'])
def esetcookie():
    loggedIn, firstName = egetLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM facility')
        itemData = cur.fetchall()
        if loggedIn == True:
            cur.execute("SELECT userId, firstName FROM eusers WHERE email = ?", (session['email'],))
            userId = cur.fetchone()[0]
        else:
            userId = None
    itemData = parse(itemData)

    global resp
    if request.method == 'POST':
        resp = make_response(render_template('employeehome.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName))
        if loggedIn == True:
            resp.set_cookie('user_id', str(userId))
            return resp
        else:
            resp.set_cookie('user_id', str(userId), max_age=0)
            return resp
    else:
        return render_template('employeehome.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName)

@auth.route('/egetcookie')
def egetcookie():
   name = request.cookies.get('user_id')
   return (f"<h1 style=\"text-align: center\">Cookie value set to: {name}</h1><a style=\"background-color: skyblue; color: black; margin-left: 800px; padding: 0px 10px 0px 10px; border-radius: 5px; text-decoration: none\" href=\"/employeehome\">Go To Employee Home</a>")
