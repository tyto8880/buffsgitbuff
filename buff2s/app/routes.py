# imports application module from app directory
from app import app
from flask import render_template, request, redirect, session

# local imports for some of that sweet sweet sugar
import app.database as db
import app.validation as validate


@app.route('/user/<user>')
def userdash(user):
    return render_template('user.html')


# base webpage
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error = None
        # handle user not present
        if validate.valid_user(request.form['username'], request.form['password']) and db.get_user_info(request.form['username'], request.form['password']):
            if not error:
                session.clear()
                session['username'] = request.form['username']
            return redirect('/user/' + request.form['username'])
    return render_template('login.html')


# signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        error = None
        # provide handling for taken user and invalid username
        if validate.valid_user(request.form['username'], request.form['password']) and not db.get_user_info(request.form['username'], request.form['password']):
            db.create_user(request.form['username'], request.form['password'])
            if not error:
                session['username'] = request.form['username']

    return render_template('signup.html')


@app.route('/logout')
def logout():
    if session['username']:
        session.clear()
    return redirect('/home')
