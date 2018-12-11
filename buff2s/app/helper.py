# simple helper function for translating array of muscles into numbers
def getMuscles(form):
    listMuscles = []
    muscleID = {
        'Misc': 0,
        'Quads': 1,
        'Hamstrings': 2,
        'Calves': 3,
        'Chest': 4,
        'Back': 5,
        'Shoulders': 6,
        'Triceps': 7,
        'Biceps': 8,
        'Forearms': 9,
        'Traps': 10,
        'Abs': 11,
        'Glutes': 12,
        'Lats': 13
    }
    for muscle in muscleID:
        if (form.get(muscle)):
           listMuscles.append(muscleID[muscle])
    return listMuscles
