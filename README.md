Sports centre booking system - Squad36
=====
The web application is build with python Flask framwork along with SQLite3 database.

The user can see the website without loging in, but to make a booking or buy a membership the user has to login/register.

The manager can register/login and edit, delete facilities, activities and see usage&sales chart. Also only the manager can add new staff mambers.

The employee login works only with the given email and password by the manager for security reasons. The employee can amend user bookings by deleting or making new ones.

For all pages you cannot use the same email twice.


## Requirements
1. Python 3.6, recommending [Anaconda](https://anaconda.org/anaconda/python)

## Setup
1. Install flask and packages
```
$ pip install flask
$ pip install flask-login
$ pip install flask-mail
$ pip install flask-migrate
$ pip install flask-wtf
$ pip install flask-babel
$ pip install flask-cors
$ pip install coverage
$ pip install requests
```
2. Database
A database is already filled in with the standard facilities and activities, so there is no need to create a new one.

# Running
1. Run the flask application from the project directory, running on localhost
```
$ flask run
```
2. Open the app in browser: [localhost](http://127.0.0.1:5000/)

# Testing the Unit Tests
```
$ pip install pytest
```
1. Run the flask environment, go into sportsCentre folder and run:
$ pytest unittests.py
