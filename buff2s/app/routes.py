# imports application module from app directory
from app import app

# import template class
from flask import render_template, request, redirect
import app.database as db
import app.validation as validate


# base webpage
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if validate.valid_user(request.form['username'], request.form['password']):
            return redirect('/user/' + request.form['username'])
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # provide handling for taken user
        if validate.valid_user(request.form['username'], request.form['password']):
            db.create_user(request.form['username'], request.form['password'])

    return render_template('signup.html')


@app.route('/user/<user>')
def userdash(user):
    return render_template('user.html')
