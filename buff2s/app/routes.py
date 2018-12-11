# imports application module from app directory
from app import app
from flask import render_template, request, redirect, session, json

# local imports for some of that sweet sweet sugar
import app.database as db
import app.validation as validate
import app.helper as helper

# import for json used in asynchronous calls
from flask import jsonify

# Should probably return user workouts
@app.route('/user/<user>', methods=['GET', 'POST'])
def userdash(user):
    userInfo = db.getUserInfo(user)
    posts = []
    # for each workout, add workout to posts that will display on page, get workoutj
    return render_template('user.html', user=userInfo, posts=posts)

# used for get workout call
@app.route('/userWorkout', methods=['POST', 'GET'])
def createWorkout():
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
            return jsonify(workout)
        except Exception as e:
            print(e)
            return 'error: create workout did not go through'
    elif (request.method == 'GET'):
        try:
            # will want to return a jsonifyed version of the workouts
            userInfo = db.getUserInfo(session['username'])
            workouts = userInfo['favoriteWorkouts']
            userWorkouts = []
            for workoutID in workouts:
                workout = db.getWorkoutFromIDForUser(int(workoutID), session['username'])
                userWorkouts.append(workout)
            return jsonify(userWorkouts)
        except:
             return 'get workout did not work correctly'
    return 'error: not get or post request'


# used for displaying workouts on page
# @app.route('/displayWorkouts', methods=['POST'])
# def displayWorkouts():

# used to add workout to database
# @app.route('/addWorkout', methods=['POST'])
# def addWorkout():

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
            return redirect('/')
    return render_template('signup.html', error=error)

@app.route( '/edit_Profile', methods=['GET', 'POST'])
def edit_Profile():
    error = None
    return render_template('edit_Profile.html')


@app.route('/logout')
def logout():
    if session['username']:
        session.clear()
    return redirect('/home')

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


