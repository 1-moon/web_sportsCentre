"""
      A file to compose page for main pages
"""

import hashlib
from flask import redirect, render_template, session, url_for, jsonify, request, current_app

import json
from . import main
import sqlite3
from .forms import parse, searchProd,getLoginDetails, mgetLoginDetails, egetLoginDetails
from flask import request
from werkzeug.wrappers import Response, Request
from werkzeug.utils import secure_filename
from datetime import datetime
from app.models import eusers, users
from app import db

#by geeyoon
#route for displaying inbox page
@main.route('/inbox')
def inbox():
    user_id = session.get('user_id')
    if not user_id:
        # redirect to login page
        return redirect(url_for('auth.loginForm'))

    # get all messages sent by current user
    messages = messages.query.filter_by(sender_id=user_id).all()

    return render_template('inbox.html', messages=messages)

#route for sending a message
@main.route('/send_message', methods = ['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        # get the form data
        sender_id = request.form.get('sender_id')
        receiver_id = request.form.get('receiver_id')
        content = request.form.get('content')
        
        # create a new message object
        new_message = messages(
            senderId=sender_id, receiverId=receiver_id, content=content, timestamp=datetime.now())

        # connect to the database
        conn = sqlite3.connect('app.db')

        # execute the query to add the message to the database
        conn.execute("INSERT INTO messages (sender_id, receiver_id, content, timestamp) VALUES (?, ?, ?, ?)", 
                     (sender_id, receiver_id, content, datetime.now()))

        # commit the transaction
        conn.commit()
        
        # close the database connection
        conn.close()
        
        return redirect(url_for('inbox'))
    
    # Get a list of all users
    all_users = eusers.query.all()
    
    # Get the current euser
    current_euser = eusers.query.filter_by(userId=1).first()
    
    return render_template('send_message.html', users=all_users, euser=current_euser)

#by ayesha
@main.route('/usage')
def usage():
    if 'email' not in session:
        return render_template('managerhome.html')
    loggedIn, firstName = mgetLoginDetails()
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    c.execute('SELECT facilityId, COUNT(*) FROM bookings GROUP BY facilityId')
    results = c.fetchall()
    c.execute('SELECT activityId, COUNT(*) FROM bookings GROUP BY activityId')
    results1 = c.fetchall()
    c.execute('SELECT activityEventId, COUNT(*) FROM bookings GROUP BY activityEventId')
    results2 = c.fetchall()
    c.execute('SELECT membershipId, COUNT(*) FROM bookings GROUP BY membershipId')
    results3 = c.fetchall()

    conn.close()

    return render_template('usage.html', results=results, results1=results1, results2=results2, results3=results3, loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route('/managerhome')
def managerhome():
  if 'email' not in session:
        return render_template('managerhome.html')
  loggedIn, firstName = mgetLoginDetails()
  return render_template("managerhome.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route('/staffmembers')
def staffmembers():
  with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM eusers")
        eusers = cur.fetchall()

  eusers = parse(eusers)
  loggedIn, firstName = getLoginDetails()
  return render_template('manager/staffmembers.html', eusers=eusers, loggedIn=loggedIn, firstName=firstName)

#by geeyoon
@main.route('/employeehome')
def employeehome():
  if 'email' not in session:
        return render_template('employeehome.html')
  loggedIn, firstName = egetLoginDetails()
  return render_template("employeehome.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route('/privacy')
def privacy():
  if 'email' not in session:
        return render_template('privacy.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("privacy.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route('/mprivacy')
def mprivacy():
  if 'email' not in session:
        return render_template('mprivacy.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("mprivacy.html", loggedIn=loggedIn, firstName=firstName)

@main.route('/payment')
def payment():
  if 'email' not in session:
        return render_template('pay/payment.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("pay/payment.html", loggedIn=loggedIn, firstName=firstName)

"""sumary_line

    profile space 
"""

#by ayesha
@main.route("/account/profile/edit")
def editProfile():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName = getLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone FROM users WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName = getLoginDetails()
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with sqlite3.connect('app.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM users WHERE email = ?", (session['email'], ))
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE users SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("changePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
    else:
        return render_template("changePassword.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha      
@main.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    if request.method == 'POST':
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
        with sqlite3.connect('app.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE users SET firstName = ?, lastName = ?, address1 = ?, address2 = ?, zipcode = ?, city = ?, state = ?, country = ?, phone = ? WHERE email = ?', (firstName, lastName, address1, address2, zipcode, city, state, country, phone, email))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('main.editProfile'),  msg=msg)
      
# Manager edit profile - by ayesha
@main.route('/personaldetails')
def personaldetails():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName = mgetLoginDetails()
    return render_template("manager/personaldetails.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route("/account/personaldetails/edit")
def meditProfile():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName = mgetLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone FROM musers WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("meditProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route("/account/personaldetails/changePassword", methods=["GET", "POST"])
def mchangePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName = mgetLoginDetails()
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with sqlite3.connect('app.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM musers WHERE email = ?", (session['email'], ))
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE musers SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("mchangePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
    else:
        return render_template("mchangePassword.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha      
@main.route("/mupdateProfile", methods=["GET", "POST"])
def mupdateProfile():
    if request.method == 'POST':
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
        with sqlite3.connect('app.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE musers SET firstName = ?, lastName = ?, address1 = ?, address2 = ?, zipcode = ?, city = ?, state = ?, country = ?, phone = ? WHERE email = ?', (firstName, lastName, address1, address2, zipcode, city, state, country, phone, email))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('main.meditProfile'))

# modified by moon 
@main.route('/membership', methods=["GET", "POST"])
def membership():
    # log-in check 
    if 'email' not in session:
        return render_template('pay/memship.html')
    loggedIn, firstName = getLoginDetails()
    if request.method == "POST":
        status = request.form['status']
        memberType = request.form['membership_type']
        with sqlite3.connect('app.db') as con:
            cur = con.cursor()
            # to retrieve the 'userId' value from the 'users' table based on the email address
            # in the 'session' object 
            cur.execute("SELECT userId FROM users WHERE email = ?",
                         (session['email'],))
            # to retrieve the first row of the result set using the 'fetchone()' method  
            row = cur.fetchone()
            userId = row[0]
            # to update these column 
            cur.execute("UPDATE users SET status=?, memberType=? WHERE userId=?",
                         (status, memberType, userId))
            # to commit for updated data 
            con.commit()
        return redirect(url_for('main.payment'))
    return render_template("pay/memship.html", loggedIn=loggedIn, firstName=firstName )

#modified by moon 
@main.route('/profile')
def profile():
    #  login check 
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName = getLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        # to retrieve userId same method above membersip decorater  
        userId = cur.execute("SELECT userId FROM users WHERE email = ?", 
                             (session['email'],))
        row = cur.fetchone()
        userId = row[0]
        # to retrieve status value 
        status = cur.execute("SELECT status FROM users WHERE userId = ? ",
                             (userId,))
        status = cur.fetchone()[0]
        # to retrieve membership value 
        if status is not None:
            status = status
        membership = cur.execute("SELECT memberType FROM users WHERE userId = ? ",
                             (userId,))
        membership = cur.fetchone()[0]
        print("membertype: ", membership)
        cur.close()
    conn.close()
    return render_template("profile.html", loggedIn=loggedIn, firstName=firstName,
                            status=status, membership=membership, userId=userId)

#firstly released by moon -
@main.route('/<int:userId>/cancelMembership', methods=['POST'])
def cancelMembership(userId):
    if 'email' not in session:
        return render_template('auth/login.html')
    loggedIn, firstName = mgetLoginDetails()
    if request.method == "POST":
        with sqlite3.connect('app.db') as con:
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            userId=int(userId)
            cur.execute('UPDATE users SET memberType = NULL, status = NULL where userId =?',
                         (userId,))
            con.commit() 
    return render_template("/profile.html",
                            loggedIn=loggedIn, firstName=firstName)


@main.route('/activities')
def activities():
  if 'email' not in session:
        return render_template('activities.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("activities.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route('/equipment')
def equipment():
  if 'email' not in session:
        return render_template('equipment.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("equipment.html", loggedIn=loggedIn, firstName=firstName)

@main.route('/cart')
def cart():
  if 'email' not in session:
        return render_template('cart.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("cart.html", loggedIn=loggedIn, firstName=firstName)

@main.route('/qna')
def qna():
  if 'email' not in session:
        return render_template('qna.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("qna.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route('/elder')
def elder():
  if 'email' not in session:
        return render_template('elder.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("elder.html", loggedIn=loggedIn, firstName=firstName)

@main.route('/hiring')
def hiring():
  if 'email' not in session:
        return render_template('hiring.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("hiring.html", loggedIn=loggedIn, firstName=firstName)

#by Natalie
@main.route('/ehiring')
def ehiring():
  if 'email' not in session:
        return render_template('ehiring.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("ehiring.html", loggedIn=loggedIn, firstName=firstName)

@main.route('/aboutUs')
def aboutUs():
  if 'email' not in session:
        return render_template('aboutUs.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("aboutUs.html", loggedIn=loggedIn, firstName=firstName)

@main.route('/maboutUs')
def maboutUs():
  if 'email' not in session:
        return render_template('maboutUs.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("maboutUs.html", loggedIn=loggedIn, firstName=firstName)

@main.route('/eaboutUs')
def eaboutUs():
  if 'email' not in session:
        return render_template('eaboutUs.html')
  loggedIn, firstName = egetLoginDetails()
  return render_template("eaboutUs.html", loggedIn=loggedIn, firstName=firstName)

@main.route('/eqna')
def eqna():
  if 'email' not in session:
        return render_template('eqna.html')
  loggedIn, firstName = egetLoginDetails()
  return render_template("eqna.html", loggedIn=loggedIn, firstName=firstName)

@main.route('/facilities')
def facilities():
  with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        #showing facility table in facility.html
        cur.execute("SELECT facilityId, name, roomCounter, description, capacity, openTime, closeTime FROM facility")
        facility = cur.fetchall()
        #team events, clases table
        cur.execute('''
        SELECT facility.name, activity.name, activity.price FROM activity
        INNER JOIN facility ON facility.facilityId = activity.facilityId
        ''')
        # Fetching rows from the result table
        result = cur.fetchall()
        #showing activity table in facility.html
        cur.execute('''
        SELECT  facility.name, activityEvent.name, activityEvent.day, activityEvent.startTime, activityEvent.endTime FROM activityEvent
        INNER JOIN facility ON activityEvent.facilityId = facility.facilityId
        ''')

# Fetching rows from the result table
        result1 = cur.fetchall()

  facility = parse(facility)
  result = parse(result)
  result1 = parse(result1)
  loggedIn, firstName = getLoginDetails()
  return render_template('facilities.html', result=result, result1=result1,facility=facility, loggedIn=loggedIn, firstName=firstName)

# See all facilities - for manager 
#by ayesha
@main.route('/mfacilities')
def mfacilities():
  with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        #showing facility table in facility.html
        cur.execute("SELECT facilityId, name, roomCounter, description, capacity, openTime, closeTime FROM facility")
        facility = cur.fetchall()
        #team events, clases table
        cur.execute('''
        SELECT facility.name, activity.name, activity.price FROM activity
        INNER JOIN facility ON facility.facilityId = activity.facilityId
        ''')
        # Fetching rows from the result table
        result = cur.fetchall()
        #showing activity table in facility.html
        cur.execute('''
        SELECT  facility.name, activityEvent.name, activityEvent.day, activityEvent.startTime, activityEvent.endTime FROM activityEvent
        INNER JOIN facility ON activityEvent.facilityId = facility.facilityId
        ''')

# Fetching rows from the result table
        result1 = cur.fetchall()

  facility = parse(facility)
  result = parse(result)
  result1 = parse(result1)
  loggedIn, firstName = mgetLoginDetails()
  return render_template('manager/mfacilities.html', result=result, result1=result1,facility=facility, loggedIn=loggedIn, firstName=firstName)

# ================== manager - delete facilities ===========================
#by ayesha
@main.route('/<int:facilityId>/Deletef', methods=['POST'])
def Deletef(facilityId):
    if 'email' not in session:
        return render_template('managerhome.html')
    loggedIn, firstName = mgetLoginDetails()
    if request.method == "POST":
        with sqlite3.connect('app.db') as con:
            con.row_factory=sqlite3.Row

            cur = con.cursor()
            facilityId=int(facilityId)
            cur.execute('DELETE from facility where facilityId =?', (facilityId,))
            con.commit() 
            # rows = cur.fetchone()
            return redirect("/mfacilities")
    return render_template("manager/managerhome.html", loggedIn=loggedIn, firstName=firstName)

# Allowing manager to edit facilities
#by ayesha
@main.route("/meditfacilities")
def meditfacilities():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName = mgetLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT facilityId, name, roomCounter description, capacity, openTime, closeTime FROM facility WHERE name = ?", (['facilityId'] ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("manager/meditfacilities.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName)

#by ayesha      
@main.route("/mupdatefacilities", methods=["GET", "POST"])
def mupdatefacilities():
    if request.method == 'POST':
        facilityId = request.form['facilityId']
        name = request.form['name']
        roomCounter = request.form['roomCounter']
        description = request.form['description']
        capacity = request.form['capacity']
        openTime = request.form['openTime']
        closeTime = request.form['closeTime']
        with sqlite3.connect('app.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE facility SET roomCounter = ?, description = ?, capacity = ?, openTime = ?, closeTime = ? WHERE name = ?', (roomCounter, description, capacity, openTime, closeTime, name))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('main.meditfacilities'), msg=msg) 

# manager - adding facilities 
#by ayesha
@main.route("/maddfacilityForm")
def maddfacilityForm():
    return render_template("manager/maddfacility.html")

@main.route("/maddfacility", methods = ['GET', 'POST'])
def maddfacility():
    loggedIn, firstName = mgetLoginDetails()
    if request.method == 'POST':
        #Parse form data
        name = request.form['name']
        roomCounter = request.form['roomCounter']
        description = request.form['description']
        capacity = request.form['capacity']
        openTime = request.form['openTime']
        closeTime = request.form['closeTime']

        with sqlite3.connect('app.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO facility (name, roomCounter, description, capacity, openTime, closeTime) VALUES (?, ?, ?, ?, ?, ?)', (name, roomCounter, description, capacity, openTime, closeTime))
                con.commit()

                msg = "Added Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("managerhome.html", error=msg, loggedIn=loggedIn, firstName=firstName)   

      
# See all activities - for manager 
#by ayesha
@main.route('/mactivities')
def mactivities():
  with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        #team events, clases table
        cur.execute('''
        SELECT facility.name, activity.name, activity.price FROM activity
        INNER JOIN facility ON facility.facilityId = activity.facilityId
        ''')
        # Fetching rows from the result table
        result = cur.fetchall()
  result = parse(result)
  loggedIn, firstName = mgetLoginDetails()
  return render_template('mactivities.html', result=result, loggedIn=loggedIn, firstName=firstName)

# Allowing manager to edit facilities
#by ayesha
@main.route("/meditactivities")
def meditactivities():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName = mgetLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT activityId, facilityId, name, price FROM activity WHERE activityId = ?", (['activityId'] ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("meditactivities.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName)

#by ayesha       
@main.route("/mupdateactivities", methods=["GET", "POST"])
def mupdateactivities():
    if request.method == 'POST':
        activityId = request.form['activityId']
        name = request.form['name']
        price = request.form['price']
        with sqlite3.connect('app.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE activity SET price = ? WHERE activityId = ?', (price, activityId))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('main.meditactivities'))

# manager - adding activities 
#by ayesha
@main.route("/maddactivityForm")
def maddactivityForm():
    return render_template("maddactivity.html")

@main.route("/maddactivity", methods = ['GET', 'POST'])
def maddactivity():
    loggedIn, firstName = mgetLoginDetails()
    if request.method == 'POST':
        #Parse form data
        name = request.form['name']
        price = request.form['price']

        with sqlite3.connect('app.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO activity (name, price) VALUES (?, ?)', (name, price))
                con.commit()

                msg = "Added Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("managerhome.html", error=msg, loggedIn=loggedIn, firstName=firstName)  
      


@main.route('/booking', methods=['GET', 'POST'])
def booking():
    loggedIn, firstName = getLoginDetails()
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    facilities = cursor.execute("SELECT facilityId, name FROM facility").fetchall()
    activities = []
    events = []

    selectedFacility = "squash"
    if request.method == 'POST':
        facility_id = request.form['facility']
        activities = cursor.execute("SELECT activityId, name FROM activity WHERE facilityId=?", (facility_id,)).fetchall()
        if request.form.get('activity'):
            activity_id = request.form['activity']
            events = cursor.execute("SELECT activityEventId, name, day, startTime FROM activityEvent WHERE facilityId=? AND activityId=?", (facility_id, activity_id)).fetchall()

            activity_type = cursor.execute("SELECT name FROM activity WHERE activityId=?", (activity_id,)).fetchone()

            if request.form.get('activity') and activity_type[0] == 'General use':
                return render_template('bookingpopup.html', loggedIn=loggedIn, firstName=firstName)
    conn.close()
    return render_template('booking.html', selectedFacility=selectedFacility, facilities=facilities, activities=activities, events=events, loggedIn=loggedIn, firstName=firstName)
      

#by ayesha
@main.route("/search_result", methods=["POST"])
def Search():
    loggedIn, firstName = getLoginDetails()
    form = searchProd()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM facility where name='{form.searched.data}'")
        fsearchData = cur.fetchall()
        if len(fsearchData) == 0:
            return render_template('search.html', fsearchData='NO ITEM', itemSear=form.searched.data, loggedIn=loggedIn, firstName=firstName)
        return render_template('search.html', fsearchData=fsearchData, itemSear=form.searched.data, loggedIn=loggedIn, firstName=firstName)
      

#manager - search 
#by ayesha
@main.route("/msearch_result", methods=["POST"])
def mSearch():
    loggedIn, firstName = mgetLoginDetails()
    form = searchProd()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM facility where name='{form.searched.data}'")
        fsearchData = cur.fetchall()
        if len(fsearchData) == 0:

            return render_template('msearch.html', fsearchData='NO ITEM', itemSear=form.searched.data, loggedIn=loggedIn, firstName=firstName)
        return render_template('msearch.html', fsearchData=fsearchData, itemSear=form.searched.data, loggedIn=loggedIn, firstName=firstName)

#employee - search 
#by ayesha
@main.route("/esearch_result", methods=["POST"])
def eSearch():
    loggedIn, firstName = egetLoginDetails()
    form = searchProd()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM facility where name='{form.searched.data}'")
        fsearchData = cur.fetchall()
        if len(fsearchData) == 0:
            return render_template('esearch.html', fsearchData='NO ITEM', itemSear=form.searched.data, loggedIn=loggedIn, firstName=firstName)
        return render_template('esearch.html', fsearchData=fsearchData, itemSear=form.searched.data, loggedIn=loggedIn, firstName=firstName)

#by Natalie
@main.route('/epayslip')
def epayslip():
  if 'email' not in session:
        return render_template('epayslip.html')
  loggedIn, firstName = egetLoginDetails()
  return render_template("epayslip.html", loggedIn=loggedIn, firstName=firstName)

#by Natalie
@main.route('/eprofile')
def eprofile():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName = egetLoginDetails()
    return render_template("eprofile.html", loggedIn=loggedIn, firstName=firstName)

#by Natalie
@main.route("/account/eprofile/edit")
def eeditProfile():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName = egetLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone, position FROM eusers WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("e_editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName)


#by Natalie
@main.route("/eupdateProfile", methods=["GET", "POST"])
def eupdateProfile():
    if request.method == 'POST':
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
        with sqlite3.connect('app.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE eusers SET firstName = ?, lastName = ?, address1 = ?, address2 = ?, zipcode = ?, city = ?, state = ?, country = ?, phone = ? position = ? WHERE email = ?', (firstName, lastName, address1, address2, zipcode, city, state, country, phone, position, email))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('main.e_editProfile'))
      
#by Natalie
@main.route("/account/eprofile/echangePassword", methods=["GET", "POST"])
def echangePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName = egetLoginDetails()
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with sqlite3.connect('app.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM eusers WHERE email = ?", (session['email'], ))
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE eusers SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("echangePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
    else:
        return render_template("echangePassword.html", loggedIn=loggedIn, firstName=firstName)

#by Natalie
@main.route('/etimetable')
def etimetable():
    if 'email' not in session:
        return render_template('etimetable.html')
    loggedIn, firstName = getLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM eusers WHERE email = ?", (session['email'],))
        user_id = cur.fetchone()[0]
        cur.execute("SELECT startTime, endTime, position, facility FROM work WHERE staffId = ?", (user_id,))
        workData = cur.fetchall()
        cur.execute("SELECT position FROM eusers WHERE email = ?", (session['email'],))
        positionData = cur.fetchone()
    conn.close()
    return render_template("etimetable.html", loggedIn=loggedIn, firstName=firstName, positionData=positionData, workData=workData)

#by Natalie
@main.route("/massignjobForm")
def massignjobForm():
    return render_template("massignjob.html")

@main.route('/massignjob', methods=['GET', 'POST'])
def massignjob():
    if 'email' not in session:
        return redirect(url_for('main.login'))
    loggedIn, firstName = mgetLoginDetails()

    if request.method == 'POST':
        userId = request.form.get('user')
        facilityId = request.form.get('facility')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')

        with sqlite3.connect('app.db') as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO work (staffId, date, startTime, endTime, facility) VALUES (?, ?, ?, ?, ?)", (userId, date.today().strftime("%Y-%m-%d"), start_time, end_time, facilityId))
            conn.commit()

        flash('Job assigned successfully!', 'success')
        return redirect(url_for('main.massignjob'))

    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM eusers")
        users = cur.fetchall()
        cur.execute("SELECT * FROM facility")
        facilities = cur.fetchall()
    conn.close()

    return render_template('massignjob.html', loggedIn=loggedIn, firstName=firstName, users=users, facilities=facilities)

###################Database########################
#this function updates the database contents
@main.route('/')
def createDbs():
  with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()

        cur.executemany("insert or replace into facility values (?,?,?,?,?,?,?)", facility_list)
        cur.executemany("insert or replace into activity values (?,?,?,?)", activity_list)
        cur.executemany("insert or replace into activityEvent values (?,?,?,?,?,?,?)", activityEvent_list)
        cur.executemany("insert or replace into membership values (?,?,?)", membership_list)
        conn.commit()
        
        cur.execute("SELECT * FROM facility")
        cur.execute("SELECT * FROM activity")
        cur.execute("SELECT * FROM activityEvent")
        cur.execute("SELECT * FROM membership")

        loggedIn, firstName = getLoginDetails()
        return render_template('index.html', loggedIn=loggedIn, firstName=firstName)

facility_list = [
  ("1", "Swimming pool", "1",  "General use, Lane swimming, Lessons, Team Events", "30", "08:00", "20:00"),
  ("2", "Fitness room", "1",  "General use", "35", "08:00", "22:00"),
  ("3", "Squash court", "2",  "1-hour sessions * (1)", "8", "08:00", "22:00"),
  ("4", "Sports hall", "1",  "1-hour sessions, Team events", "45", "08:00", "22:00"),
  ("5", "Climbing wall", "1",  "General use", "22", "10:00", "22:00"),
  ("6", "Studio", "1",  "Classes: Pilates, Aerobics, Yoga", "25", "08:00", "22:00")
]

activity_list = [
  #swimming pool
  ("1", "1", "General use", "15"),
  ("2", "1", "Lane swimming", "15"),
  ("3", "1", "Lessons", "15"),
  ("4", "1", "Team Events", "15"),
  #fitness room
  ("5", "2", "General use", "15"),
  #squash court
  ("6", "3", "1-hour sessions", "15"),
  #sports hall
  ("7", "4", "1-hour sessions", "15"),
  ("8", "4", "Team Events", "15"),
  #climbing wall
  ("9", "5", "General use", "15"),
  #studio
  ("10", "6", "Exercise classes: Pilates", "15"),
  ("11", "6", "Exercise classes: Aerobics", "15"),
  ("12", "6", "Exercise classes: Yoga ", "15")
]

activityEvent_list = [
  #swimming pool
  ("1", "4", "1", "Team Events", "Friday", "08:00", "10:00"),
  ("2", "4", "1", "Team Events", "Sunday", "08:00", "10:00"),
  #sports hall
  ("3", "8", "4", "Team Events", "Tuesday", "19:00", "21:00"),
  ("4", "8", "4", "Team Events", "Saturday", "09:00", "11:00"),

  #studio pilates
  ("5", "10", "6", "Pilates", "Monday", "18:00", "19:00"),
  #studio aerobics
  ("6", "11", "6", "Aerobics", "Tuesday", "10:00", "11:00"),
  ("7", "11", "6", "Aerobics", "Thursday", "19:00", "20:00"),
  ("8", "11", "6", "Aerobics", "Saturday", "10:00", "11:00"),
  #studio yoga
  ("9", "12", "6", "Yoga", "Friday", "19:00", "20:00"),
  ("10", "12", "6", "Yoga", "Sunday", "09:00", "10:00")

]

membership_list = [
  ("1", "Monthly", "35"),
  ("2", "Annual", "300")
  
]
###################Database########################

