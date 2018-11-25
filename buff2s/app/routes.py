# imports application module from app directory
from app import app

# import template class
from flask import render_template, request
# from app.forms import LoginForm
import app.database as db
import app.validation as validate


# base webpage
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/login')
def login():
    # form = LoginForm()
    return render_template('login.html', title='Sign In')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if validate.valid_user(request.form['username'], request.form['password']):
            db.create_user(request.form['username'], request.form['password'])

    return render_template('signup.html', title='Sign Up')
