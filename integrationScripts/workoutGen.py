#import sys
#print(sys.version)
import pymongo
import heapq

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

EXPLORATION_REWARD = 100.0#what is the extra reward given for trying a new exercise?
EXERCISE_DROP_PROBABILITY = 0.05#when creating a workout, what is the chance that we ignore the current optimal?

"""
user is the actual item from the database
time is a range of acceptable times, stored as a tuple of (min,max); IGNORED FOR NOW
muscles is a list of desired muscle ids to get

this version won't look for existing workouts yet
"""
def createWorkout(user, time, muscles):
	viableExercises = db.exercises.find({})

	dropCardioThreshold = user["cardio"]#anything over this threshold is automatically not included
	dropStrengthThreshold = user["strength"]#maybe make these more complex

	includedExercises = []#maxheap of exercises

	for exercise in viableExercises:
		#trim down the set to only the viable ones
		include = False
		if (exercise["difficultyCardio"] <= dropCardioThreshold) and (exercise["difficultyStrength"] <= dropStrengthThreshold):
			for exerciseMuscle in db.exercies["muscles"]:
				if exerciseMuscle in muscles:
					include = True
		if include:
			exercisePriority = 0.0
			reps = 12
			if exercise["exerciseid"] in user["favoriteExercises"]:
				#
				userFavorite = user["favoriteExercises"].index(exercise["exerciseid"])
				exercisePriority = user["favoriteExercises"][userFavorite][1] + 1.0/userFavorite#assuming favoriteExercises is sorted in order of "favorite"ness
				reps = user["favoriteExercises"][userFavorite][2]
			else:
				exercisePriority = EXPLORATION_REWARD - (user["cardio"] - exercise["difficultyCardio"])**2 - (user["strength"] - exercise["difficultyStrength"])**2
				#exercise priority for an untried exercise is the default reward minus the difference between the user's levels in strength and cardio and the exercise's
			heappush(includedExercises,(exercisePriority,(exercise,reps)))

	numOfSetsInWorkout = 4 + (user["cardio"])#how many sets in the workout? Ideally, this will be a more complex function of strength, cardio, time, etc.
	workout = []
	totalTime = 0

	for setIndex in range(numOfSetsInWorkout):
		#generate a new set
		setTemp = []
		exercisesInSet = 2 + int(user["cardio"]/4)
		for ex in range(exercisesInSet):
			exerciseTuple = heappop(includedExercises)
			if random.uniform(0,1) >= EXERCISE_DROP_PROBABILITY:
				setTemp.append(exerciseTuple[1])
		workout.append(setTemp)
	return workout