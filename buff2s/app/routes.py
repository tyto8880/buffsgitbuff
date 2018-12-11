# imports application module from app directory
from app import app
from flask import render_template, request, redirect, session, json, jsonify

# local imports for some of that sweet sweet sugar
import app.database as db
import app.validation as validate
import app.helper as helper

# base webpage, index
@app.route('/')
def root():
    return render_template('home.html', title='Home')

# cleans up home/root disparity
@app.route('/home')
def home():
    return redirect('/')

# login page, takes a post request to see if a user exists that can be logged in
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        # handle user not present
        if validate.valid_user(request.form['username'], request.form['password']) and db.validateUser(request.form['username'], request.form['password']):
            # if user exists, logs them in and directs them to user page
            session.clear()
            session['username'] = request.form['username']
            return redirect('/user/' + request.form['username'])
        else:
            error = 'Username/password is incorrect!'
    # if not post (want to log in), simply returns login page to do so
    return render_template('login.html', error=error)

# logout page, simply clears session and redirect to home page
@app.route('/logout')
def logout():
    if session['username']:
        session.clear()
    return redirect('/home')

# signup page, to create an account
@app.route('/signup', methods=['POST', 'GET'])
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
            # if signed up, logs in and directs back to home
            session['username'] = request.form['username']
            return redirect('/')
    return render_template('signup.html', error=error)

# base html page for user page
@app.route('/user/<user>')
def userdash(user):
    userInfo = db.getUserInfo(user)
    return render_template('user.html', user=userInfo)

# edit profile page, no real functionality
@app.route( '/edit_Profile')
def edit_Profile():
    return render_template('edit_Profile.html')

# call for create and return a workout to user page
# doesnt return an actual webapge, just handles user.html calls
@app.route('/userWorkout', methods=['POST', 'GET'])
def createWorkout():
    # create workout call
    if request.method == 'POST':
        try:
            muscles = helper.getMuscles(request.form)
            input = request.form['exerciseClass']
            if (input == 'option1'):
                 exerciseClass = 'strength'
            else:
                exerciseClass = 'cardio'
            name = request.form.get('workoutName')
            workoutID = db.createWorkout(muscles, exerciseClass, name)
            workout = db.getWorkoutFromIDForUser(workoutID, session['username'])
            # returns json object of created workout in database
            return jsonify(workout)
        except Exception as e:
            print(e)
            return 'error: create workout did not go through'
    # call for get the users workouts
    elif (request.method == 'GET'):
        try:
            userInfo = db.getUserInfo(session['username'])
            workouts = userInfo['favoriteWorkouts']
            userWorkouts = []
            for workoutID in workouts:
                workout = db.getWorkoutFromIDForUser(int(workoutID), session['username'])
                userWorkouts.append(workout)
            # returns all user favorite workouts if they exist
            return jsonify(userWorkouts)
        except Exception as e:
             print(e)
             return 'get workout did not work correctly'
    return 'error: not get or post request'

# handles add workout to user favorites calls from userpage
@app.route('/addWorkout', methods=['POST'])
def addWorkout():
    #adds workout to current session username
    try:
        workoutID = request.form['id']
        db.addWorkoutToUserFavorites(workoutID, session['username'])
        return 'added workout'
    except Exception as e:
        print(e)
        return 'workout not added'
