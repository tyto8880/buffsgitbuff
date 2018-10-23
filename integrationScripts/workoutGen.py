#import sys
#print(sys.version)
import pymongo
# import heapq

client = pymongo.MongoClient("localhost",27017)
db = client.test

user = db.users.find()[0]
time = None
muscleGroups = ["arms"]

# print(db.testCollection.find()[0]["x"])#get the zeroth item from the database and print its value for the key "x"

"""
expect the exercise coll to look like:

primary key: "exercise name" or exerciseid
"baseReps": <float>//float to make sure we can deal with continuous exercises such as "run for 10 minutes"
"baseSets": <int>
"difficultyCardioMult": <float>
"difficultyStrengthMult": <float>
"muscleGroups": <list of str>
"timePerRep": <float>

expect the workout coll to look like:

primary key: workoutid
"sets": <list of (<list of (exercises [foreign key], reps [float])>,sets [int])>
"difficultyCardio": <float elt (0,10]>
"difficultyStrength": <float elt (0,10]>

expect the user coll to look like:

primary key: userid
"favoriteExercises": <list of (exercise [foreign key],timeSinceLastDone [int, days], lastReps)>
OR
"favoriteWorkouts": <list of (workout [foreign key],timeSinceLastDone [int, days], rating [float or int elt [0,100]]>
"passhsh": <password hash str>
"cardio": <float elt (0,10]>
"strength": <float elt (0,10]>

"""

REST_TIME_BASE_SET = 5*60#seconds
REST_TIME_BASE_REP = 40#seconds
EXERCISE_DROP_PROBABILITY = 0.05

"""
user is the actual item from the database
time is a range of acceptable times, stored as a tuple of (min,max); IGNORED FOR NOW
muscles is a list of desired muscle ids to get

this version won't look for existing workouts yet
"""
def createWorkoutWeights(user, time, muscles):
	viableExercises = db.exercises.find({"exerciseClass":"strength"})

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
		numSets = exc["baseSets"] * (user["cardio"] / 10) * (10 / (user["strength"]))
		numReps = exc["baseReps"] * (user["cardio"] / 10) * (10 / (user["strength"]))
		ttimeTemp = totalTime exc["timePerBaseSet"] * (exc["baseSets"] / numSets) + (REST_TIME_BASE_REP * (10 / user["cardio"]))
		ttimeTemp += REST_TIME_BASE / user["cardio"]
		if not((ttimeTemp > time[1]) and not (len(includedExercises) == 0)):
			workout.append(exc)
			totalTime = ttimeTemp
		
	return workout