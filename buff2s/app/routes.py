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
def root():
    return render_template('home.html', title='Home')


# cleans up home/root disparity
@app.route('/home')
def home():
    return redirect('/')


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # handle user not present
        if validate.valid_user(request.form['username'], request.form['password']) and db.validateUser(request.form['username'], request.form['password']):
            session.clear()
            session['username'] = request.form['username']
            return redirect('/user/' + request.form['username'])
        else:
            error = 'Username/password is incorrect!'
    return render_template('login.html', error=error)


# signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        # provide handling for taken user and invalid username
        if validate.valid_user(request.form['username'], request.form['password']):
            if not db.createUser(request.form['username'], request.form['email'], request.form['password']):
                error = 'Username already taken!'
        else:
            error = 'Invalid username/password!'
        if not error:
            session['username'] = request.form['username']

    return render_template('signup.html', error=error)


@app.route('/logout')
def logout():
    if session['username']:
        session.clear()
    return redirect('/home')
