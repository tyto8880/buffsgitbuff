#import sys
#print(sys.version)
import pymongo
# import heapq

client = pymongo.MongoClient("localhost",27017)
db = client.test

REST_TIME_BASE_SET = 5*60#seconds
REST_TIME_BASE_REP = 40#seconds
EXERCISE_DROP_PROBABILITY = 0.05

"""
user is the actual item from the database
time is a range of acceptable times, stored as a tuple of (min,max); IGNORED FOR NOW
muscles is a list of desired muscle ids to get
"""
def createWorkout(user, time, muscles, isWeights):
	if(isWeights):
		viableExercises = db.exercises.find({"exerciseClass":"strength"})
	else:
		viableExercises = db.exercises.find({"exerciseClass":"cardio"})

	# dropCardioThreshold = user["cardio"]#anything over this threshold is automatically not included
	# dropStrengthThreshold = user["strength"]#maybe make these more complex

	includedExercises = []#maxheap of exercises

	for exercise in viableExercises:
		#trim down the set to only the viable ones
		include = False
		for exerciseMuscle in db.exercies["muscles"]:
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
			heappush(includedExercises,(exercisePriority,exercise))

	workout = []
	totalTime = 0

	while(totalTime < time[0]):
		while(random.uniform(0,1) < EXERCISE_DROP_PROBABILITY):
			heappop(includedExercises)
		exc = heappop(includedExercises)[1]
		if(isWeights):
			numSets = exc["baseSets"] * (user["cardio"] / 10) * (10 / (user["strength"]))
			numReps = exc["baseReps"] * (user["cardio"] / 10) * (10 / (user["strength"]))
			ttimeTemp = totalTime exc["timePerBaseSet"] * (exc["baseSets"] / numSets) + (REST_TIME_BASE_REP * (10 / user["cardio"]))
			ttimeTemp += REST_TIME_BASE / user["cardio"]
		else:
			if exc["unitType"] == "time":
				time = exc["baseTime"] * (user["cardio"] / 10)
			else:
				#dist
				time = (exc["baseSpeed"] / exc["baseDist"]) * (user["cardio"] / 10)#endurance here?
			ttimeTemp = time + REST_TIME_BASE / user["cardio"]
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
	isWeights = workout[0][0]["exerciseClass"] == "strength"
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
