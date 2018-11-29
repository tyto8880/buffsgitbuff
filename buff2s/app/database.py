import pymongo
from passlib.hash import pbkdf2_sha256 as pl
# import heapq as hq
import numpy as np
from scipy import stats

client = pymongo.MongoClient("localhost", 27017)
db = client.buffs

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
		return False
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
						"cardioLevel": -1,
						"strengthLevel": -1})
	return True


# delete this user. Don't do anything if it doesn't exist or they had the wrong password
def delUser(uname, pwd):
	q = db.Users.find_one({"username":uname})
	if (q is None) or not pl.verify(pwd,q["passwordHash"]):
		return False
	db.Users.deleteOne({"_id":q["_id"]})

def exerciseInUserFavorites(user,exercise):
	favs = user["favoriteWorkouts"]
	for workout in favs:
		if exercise["exerciseID"] in workout["exercises"]:
			return True
	return False


"""
required functions:
getWorkout(wid,user): takes workout id returns proper formatted workout; save to database
createWorkout(muscles): takes muscle list and generates db collection workout object
XX dropWorkoutFromUserFavorites(wid,user): drops a workout from a user's favorites
addWorkoutToUserFavorites(wid,user): Add the workout with id wid to user's favorites
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
		return False #either the user or the workout didn't exist

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

		wkt["exercises"].append(exercise)

		#want to have mu st mu for someone whose C and S levels is the same as the recommendation
		#if C == S, mu = recommended
		#if C == 1 and S == 10, mu is low
		#if C == 10 and S == 1, mu is high
		#cap mu at something like 3x or 4x recommended
		if(wkclass == 'strength'):
			#randomly generate sets and reps according to a normal distribution with mean = 10 * BASE * (cardio / strengh) and stdev = (cardio + strength)/20
			muSets = (1./5.) * float(exercise["baseSets"]) * (float(user["cardioLevel"])/float(user["strengthLevel"]))
			muReps = (1./5.) * float(exercise["baseReps"]) * (float(user["cardioLevel"])/float(user["strengthLevel"]))
			sig = float(user["cardioLevel"] + user["strengthLevel"])/20.
			sets = int(round(stats.norm.rvs(loc=muSets,scale=sig,size=1)[0],0))
			reps = int(round(stats.norm.rvs(loc=muReps,scale=sig,size=1)[0],0))
			if sets < 1:
				sets = 1
			if reps < 1:
				reps = 1
			wkt["sets"].append(sets)
			wkt["reps"].append(reps)
		if(wkclass == 'cardio'):
			muTime = 10. * float(exercise["baseTime"]) * (float(user["cardioLevel"])/float(user["strengthLevel"]))
