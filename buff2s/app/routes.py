# imports application module from app directory
from app import app

# import template class
from flask import render_template, session, request, url_for, flash, redirect
from app.forms import LoginForm


# base webpage
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == "POST":
            if request.form['username'] == "Aaron":
                session['logged_in'] = True
                session['username'] = request.form['username']
                return redirect(url_for('home'))
            else:
                flash("No!")

    except Exception as e:
        flash(e)
        return render_template('login.html', title='Sign In')

    return render_template('login.html', title='Sign In')


@app.route('/signup')
def test():
    # return render_template('home.html', title='Home')
    return app.send_static_file('signup.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    flash("Logged Out")
    return render_template('home.html')
