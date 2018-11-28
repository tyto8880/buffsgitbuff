import pymongo
from passlib.hash import pbkdf2_sha256 as pl
import heapq as hq
import numpy as np

client = pymongo.MongoClient("localhost", 27017)
db = client.buffs

BASE_TIME_PER_REP = 3#seconds
REST_TIME_BASE_SET = 5*60  # seconds
REST_TIME_BASE_REP = 40  # seconds
EXERCISE_DROP_PROBABILITY = 0.05


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
TODO: Refactor this
need to have specific workouts look like dict:

{
"exercises":[] of workouts,
"muscles":[] of 
}
need output to look like a workout object from database collection workouts

user is the actual item from the database
time is a range of acceptable times, stored as a tuple of (min,max); IGNORED FOR NOW
muscles is a list of desired muscle ids to get
"""

'''
def createWorkout(user, time, muscles, isWeights):
	if(isWeights):
		viableExercises = db.exercises.find({"exerciseClass":"strength"})
	else:
		viableExercises = db.exercises.find({"exerciseClass":"cardio"})

	includedExercises = []#maxheap of exercises

	for exercise in viableExercises:
		#trim down the set to only the viable ones
		include = False
		for exerciseMuscle in db.exercises["muscles"]:
			if exerciseMuscle in muscles:
				include = True
		if include:
			#TODO: get rid of buffs.users["favoriteExercises"] references
			exercisePriority = 0.0
			if exerciseInUserFavorites(user,exercise):
				exercisePriority = 2
			else:
				exercisePriority = 1
			hq.heappush(includedExercises,(exercisePriority,exercise))

	workout = []
	totalTime = 0

	while(totalTime < time[0]):
		while(np.random.uniform(0,1) < EXERCISE_DROP_PROBABILITY):
			hq.heappop(includedExercises)
		exc = hq.heappop(includedExercises)[1]
		if(isWeights):
			numSets = exc["baseSets"] * (user["cardioLevel"] / 10) * (10 / (user["strengthLevel"]))
			numReps = exc["baseReps"] * (user["cardioLevel"] / 10) * (10 / (user["strengthLevel"]))
			ttimeTemp = totalTime + numReps*BASE_TIME_PER_REP/user["cardioLevel"] + (exc["baseSets"] / numSets) + (REST_TIME_BASE_REP * (10 / user["cardioLevel"]))
			ttimeTemp += REST_TIME_BASE_SET / user["cardioLevel"]
		else:
			time = exc["baseTime"] * (user["cardioLevel"] / 10)
			ttimeTemp = time + REST_TIME_BASE_SET / user["cardioLevel"]
		if not((ttimeTemp > time[1]) and not (len(includedExercises) == 0)):
			workout.append(exc["exerciseName"])
			totalTime = ttimeTemp
	return workout

"""
workout var is list of [exercise,sets,reps] or [exercise,time(s) or dist(m)] like generated above
want to use user's preferred units, base units are si
"""
def workoutToStringList(workout,user):
	wkt = []
	isWeights = workout[0][0]["exerciseClass"] == "strength"
	isDist = False
	for exercise in workout:
		excname = exercise[0]["exerciseName"]
		if isWeights:
			excq = exercise[1] + "x" + exercise[2]
		else:
			excq = exercise[1] + " sec" if exercise[1] < 60 else ((exercise[1] / 60) + " min" if ((exercise[1]/60) < 60) else (exercise[1]/3600) + " hr")
		wkt.append(excname + ", " + excq)
	return wkt
'''