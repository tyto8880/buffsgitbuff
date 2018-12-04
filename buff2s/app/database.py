import pymongo
from passlib.hash import pbkdf2_sha256 as pl
# import heapq as hq
import numpy as np
from scipy import stats
import random

client = pymongo.MongoClient("localhost", 27017)
db = client.test

BASE_TIME_PER_REP = 3#seconds
REST_TIME_BASE_SET = 5*60  # seconds
REST_TIME_BASE_REP = 40  # seconds
EXERCISE_DROP_PROBABILITY = 0.05

class ExerciseNotDefinedException(Exception):
	def __init__(self, text):
		self.ermsg = text

	def __str__(self):
		return repr(self.ermsg)

"""
Check that the user both exists and has the correct password
"""
def validateUser(uname,pwd):
	info = db.users.find_one({"username":uname})
	if not info or (info and not pl.verify(pwd,info["passwordHash"])):
		return False
	return True

"""
uname is the user's username
pwd is the user's password (not sure if we'd pass this or just the password hash to the server)
"""
def getUserInfo(uname):
	info = db.users.find_one({"username": uname})
	if not info:
		return None
	return info


# may need to also pass other settings here
def createUser(uname, email, pwd):
	if db.users.find_one({"username": uname}) is not None:
		# a user with this username already exists
		return False

	passwordHash = pl.hash(pwd)  # salt included in the hash
	db.users.insert_one({"username": uname,
						 "email":email,
						"passwordHash": passwordHash,
						"favoriteWorkouts": [],
						"cardioLevel": 1,
						"strengthLevel": 1,
						 "super":False})
	return True


# delete this user. Don't do anything if it doesn't exist
def deleteUser(uname):
	q = db.users.find_one({"username":uname})
	if q is None:
		return False
	db.users.delete_one({"_id":q["_id"]})
	return True

def updateUserCardioLevel(uname,level):
	user = db.users.find_one({"username":uname})
	if user is None:
		return False
	if (level < 1) or ((level > 10) and not ("super" in user and user["super"])):
		return False
	db.users.update_one({"_id":user["_id"]},{"$set":{"cardioLevel":level}})
	return True

def updateUserStrengthLevel(uname,level):
	user = db.users.find_one({"username":uname})
	if user is None:
		return False
	if (level < 1) or ((level > 10) and not ("super" in user and user["super"])):
		return False
	db.users.update_one({"_id":user["_id"]},{"$set":{"strengthLevel":level}})
	return True

'''
I don't think this method's going to end up being used, so it's commented out for now. --Daniel
'''
'''
def exerciseInUserFavorites(user,exercise):
	favs = user["favoriteWorkouts"]
	for workout in favs:
		if exercise["exerciseID"] in workout["exercises"]:
			return True
	return False
'''

"""
required functions:
X getWorkout(wid,user): takes workout id returns proper formatted workout; save to database
createWorkout(muscles): takes muscle list and generates db collection workout object
X addWorkoutToUserFavorites(wid,user): Add the workout with id wid to user's favorites
"""

"""
Add the workoutID to this user's list of favorite workouts.
"""
def addWorkoutToUserFavorites(workoutID, username):
	#get the actual dicts associated with this workout and username
	user = db.users.find_one({"username":username})
	workout = db.workouts.find_one({"_id":workoutID})

	if not (user and workout):
		return False #either the user or the workout didn't exist

	favs = user["favoriteWorkouts"]
	favs.append(workoutID)
	db.users.update_one({"_id":user["_id"]},{"$set":{"favoriteWorkouts":favs}})
	return True

"""
Get the workout with this id and generate the user-specific values for sets and reps, returned as a dictionary with format:

{
"workoutID" : _id of workout in datbase,
"exercises" : [] of exercise NAMES, in order,
"sets" : [] of ints corresponding to the number of sets for each exercise, same order as exercises [OPTIONAL; for strength],
"reps" : [] of ints corresponding to the number of reps for each exercise, same order as exercises [OPTIONAL; for strength],
"times" : [] of ints (units: seconds) corresponding to the length of time to do a certain exercise [OPTIONAL; for cardio]
}
"""
def getWorkoutFromIDForUser(workoutID,username):
	user = db.users.find_one({"username": username})
	workout = db.workouts.find_one({"_id": workoutID})
	if not (user and workout):
		return None #either the user or the workout didn't exist

	wkclass = workout["exerciseClass"]
	wkt = {}
	if wkclass == 'strength':
		wkt = {"workoutName":workout["workoutName"],
			   "workoutID":workoutID,
			   "exercises":[],
			   "sets":[],
			   "reps":[],}
	if wkclass == 'cardio':
		wkt = {"workoutName":workout["workoutName"],
			   "workoutID":workoutID,
			   "exercises":[],
			   "times":[]}

	#complicated bit, this is where we do the scaling
	for exerciseID in workout["exercises"]:
		#scale each exercise's sets & reps or times
		exercise = db.exercises.find_one({"_id":exerciseID}) #get the actual dict
		if not exercise:
			raise ExerciseNotDefinedException("Exercise with id " + exerciseID + " was not found during building of workout.")

		wkt["exercises"].append(exercise["exerciseName"])

		#want to have mu st mu for someone whose C and S levels is the same as the recommendation
		#if C == S, mu = recommended
		#if C == 1 and S == 10, mu is low
		#if C == 10 and S == 1, mu is high
		#cap mu at something like 3x or 4x recommended
		if(wkclass == 'strength'):
			#randomly generate sets and reps according to a truncated normal distribution
			#a = 1
			#bs = 3*Bs
			#br = 4*Br
			muSets = (5./float(user["strengthLevel"])) + float(exercise["baseSets"]) - 1.
			muReps = (5./float(user["strengthLevel"])) + float(exercise["baseReps"]) - 1.
			a = 1.
			bSets = 3.*float(exercise["baseSets"])
			bReps = 4.*float(exercise["baseReps"])
			sigSets = float(exercise["baseSets"])/4.
			sigReps = float(exercise["baseReps"])/4.
			sets = int(round(stats.truncnorm.rvs(a,bSets,loc=muSets,scale=sigSets,size=1)[0],0))
			reps = int(round(stats.truncnorm.rvs(a,bReps,loc=muReps,scale=sigReps,size=1)[0],0))
			if sets < 1:
				sets = 1
			if reps < 1:
				reps = 1
			wkt["sets"].append(sets)
			wkt["reps"].append(reps)
		if(wkclass == 'cardio'):
			muTime = (float(user["cardioLevel"])/5.) + float(exercise["baseTime"]) - 1.
			a = 1.
			bTime = 10.*float(exercise["baseTime"])
			sigTime = float(exercise["baseTime"])/4.
			time = int(round(stats.truncnorm.rvs(a, bTime, loc=muTime, scale=sigTime, size=1)[0], 0))
			wkt["times"].append(time)
	return wkt

"""
Take a list of desired muscle groups (list of muscleIDs) to hit and make a generalized workout object. Insert that into the database and return its id.
"""
def createWorkout(muscleIDs, exerciseClass, workoutName):
	#move the list of muscle ids to a list of actual muscle objects/dicts
	# muscles = [db.muscles.find_one({"_id":muscleID}) for muscleID in muscleIDs]
	muscleIDs = set(muscleIDs)
	allExercises = db.exercises.find({})
	viableExercises = []
	for exercise in allExercises:
		#trim this down to only the ones we care about
		if exercise["exerciseClass"] == exerciseClass:
			musclesMatch = False
			mlist = [exercise["muscles"]] if type(exercise["muscles"]) == float else exercise["muscles"]
			for m in mlist:
				if m in muscleIDs:
					musclesMatch = True
					break
			if musclesMatch:
				viableExercises.append(exercise)

	#how long should the workout be?
	#take a random variable for length according to TN(a=1,b=len(viableExercises),mu=6,sig=2)
	workoutLength = int(round(stats.truncnorm.rvs(1,len(viableExercises),loc=6,scale=2),0))
	random.shuffle(viableExercises)
	exercises = [int(viableExercises[i]["_id"]) for i in range(min(len(viableExercises),workoutLength))]
	existing = db.workouts.find_one({"exercises":exercises})
	if existing is not None:
		return existing["_id"]
	insertInfo = db.workouts.insert_one({"exercises":exercises,"muscles":list(muscleIDs),"exerciseClass":exerciseClass,"workoutName":workoutName})
	return insertInfo.inserted_id
