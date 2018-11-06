# imports application module from app directory
from app import app

# import template class
from flask import render_template
from app.forms import LoginForm


# base webpage
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)


@app.route('/signup')
def test():
    # return render_template('home.html', title='Home')
    return app.send_static_file('signup.html')
