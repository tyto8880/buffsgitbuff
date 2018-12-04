from app import database as db

"""
This part is more esoteric testing, so it's not going to be automated for now. If anyone thinks of a way to automate this part, go for it.
"""

#initialize a few things in the database so everything hereafter goes smoothly
db.createUser("Bobb","email","password")
db.updateUserCardioLevel("Bobb",4)
db.updateUserStrengthLevel("Bobb",8)

#first up: test the create workout function. There aren't any in the raw db, so this is necessary
wid = db.createWorkout([1,2,3],"strength","Leggg 01")
print("Simple leg workout creation; id maps to ",wid)
wkt = db.getWorkoutFromIDForUser(wid,"Bobb")
print("Strength workout for Bobb (cardio 4, strength 8) ",wkt)

# wid = db.createWorkout([])