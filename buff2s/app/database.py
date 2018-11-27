import pymongo
from passlib.hash import pbkdf2_sha256 as pl
import heapq as hq
import numpy as np

client = pymongo.MongoClient("localhost", 27017)
db = client.test

REST_TIME_BASE_SET = 5*60  # seconds
REST_TIME_BASE_REP = 40  # seconds
EXERCISE_DROP_PROBABILITY = 0.05


"""
uname is the user's username
pwd is the user's password (not sure if we'd pass this or just the password hash to the server)
"""
def get_user_info(uname, pwd):
	info = db.users.find_one({"username": uname})

	if not info or info and not pl.verify(pwd, info["pwh"]):
		return False

	return info


# may need to also pass other settings here
def create_user(uname, pwd):
	if db.users.find_one({"username": uname}) is not None:
		# a user with this username already exists
		return False
	
	pwh = pl.hash(pwd)  # salt included in the hash
	db.users.insert_one({"username": uname,
						"pwh": pwh,
						"favoriteExercises": [],
						"cardio": -1,
						"strength": -1})
	return True


# delete this user. Don't do anything if it doesn't exist or they had the wrong password
def del_user(uname, pwd):
	q = db.Users.find_one({"username":uname})
	if (q is None) or not pl.verify(pwd,q["pwh"]):
		return False
	db.Users.deleteOne({"_id":q["_id"]})


"""
user is the actual item from the database
time is a range of acceptable times, stored as a tuple of (min,max); IGNORED FOR NOW
muscles is a list of desired muscle ids to get
"""
def createWorkout(user, time, muscles, isWeights):
	if(isWeights):
		viableExercises = db.strengthExercises.find({})
	else:
		viableExercises = db.cardioExercises.find({"exerciseClass":"cardio"})

	includedExercises = []#maxheap of exercises

	for exercise in viableExercises:
		#trim down the set to only the viable ones
		include = False
		for exerciseMuscle in db.exercises["muscles"]:
			if exerciseMuscle in muscles:
				include = True
		if include:
			exercisePriority = 0.0
			if exercise["exerciseid"] in user["favoriteExercises"]:
				#
				userFavorite = user["favoriteExercises"].index(exercise["exerciseid"])
				exercisePriority = user["favoriteExercises"][userFavorite][1] + 1.0/userFavorite#assuming favoriteExercises is sorted in order of "favorite"ness
				reps = user["favoriteExercises"][userFavorite][2]
			else:
				exercisePriority = 100
			hq.heappush(includedExercises,(exercisePriority,exercise))

	workout = []
	totalTime = 0

	while(totalTime < time[0]):
		while(np.random.uniform(0,1) < EXERCISE_DROP_PROBABILITY):
			hq.heappop(includedExercises)
		exc = hq.heappop(includedExercises)[1]
		if(isWeights):
			numSets = exc["baseSets"] * (user["cardio"] / 10) * (10 / (user["strength"]))
			numReps = exc["baseReps"] * (user["cardio"] / 10) * (10 / (user["strength"]))
			ttimeTemp = totalTime + exc["timePerBaseSet"] * (exc["baseSets"] / numSets) + (REST_TIME_BASE_REP * (10 / user["cardio"]))
			ttimeTemp += REST_TIME_BASE_SET / user["cardio"]
		else:
			if exc["unitType"] == "time":
				time = exc["baseTime"] * (user["cardio"] / 10)
			else:
				#dist
				time = (exc["baseSpeed"] / exc["baseDist"]) * (user["cardio"] / 10)#endurance here?
			ttimeTemp = time + REST_TIME_BASE_SET / user["cardio"]
		if not((ttimeTemp > time[1]) and not (len(includedExercises) == 0)):
			workout.append([exc])
			totalTime = ttimeTemp
	return workout

"""
workout var is list of [exercise,sets,reps] or [exercise,time(s) or dist(m)] like generated above
want to use user's preferred units, base units are si
"""
def workoutToStringList(workout,user):
	wkt = []
	isWeights = workout[0][0] in db.strengthExercises.find({})
	isDist = False
	if not isWeights:
		isDist = workout[0][0]["unitType"] == "distance"
	for exercise in workout:
		excname = exercise[0]["exercise"]
		if isWeights:
			excq = exercise[1] + "x" + exercise[2]
		else:
			if isDist:
				excq = exercise[1] + " m" if exercise[1] < 1000 else exercise[1] + " km"
			else:
				excq = exercise[1] + " sec" if exercise[1] < 60 else ((exercise[1] / 60) + " min" if ((exercise[1]/60) < 60) else (exercise[1]/3600) + " hr")
		wkt.append(excname + ", " + excq)
	return wkt