// This script will drop the database and resupply it all at once
// NO NEED TO DROP ANYTHING BEFORE RUN SCRIPT
// if want to use another db, simply switch with test
use buffs;
// used to clear if any data already there
db.dropDatabase();
// if any of the below formats change, use a search and replace for easy fixes
// exercises insert
//for some reason insertOne wasn't working on my machine. Changed to insert()
//anything with a sidedness is assumed to give reps per side
try {
db.exercises.insert( [
        {_id: 1, exerciseName: "Arm Curl", equipment: [4, 8, 13, 25, 59, 82], muscles: 8, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 2, exerciseName: "Back Extension", equipment: [11, 22, 86, 57], muscles: 5, baseSets: 3, baseReps: 15, baseTime: 1, exerciseClass : "strength"},
        {_id: 3, exerciseName: "Badminton", equipment: 65, muscles: [1, 2, 3], baseSets: 1, baseReps: 1, baseTime: 600, exerciseClass : "cardio"},
        {_id: 4, exerciseName: "Bench Press", equipment: [13, 15, 25], muscles: [4, 7, 8], baseSets: 3, baseReps: 10, baseTime: 1, exerciseClass : "strength"},
        {_id: 5, exerciseName: "Cable Crunch", equipment: [4, 19], muscles: 11, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 6, exerciseName: "Cable Press", equipment: [4, 19], muscles: [4, 7, 8], baseSets: 3, baseReps: 20, baseTime: 1, exerciseClass : "strength"},
        {_id: 7, exerciseName: "Calf Raise", equipment: [13, 86], muscles: 3, baseSets: 2, baseReps: 60, baseTime: 1, exerciseClass : "strength"},
        {_id: 8, exerciseName: "Chest Press", equipment: [21, 19, 30, 37], muscles: 4, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 9, exerciseName: "Clean", equipment: [13, 48], muscles: [1, 2, 12], baseSets: 5, baseReps: 5, baseTime: 1, exerciseClass : "strength"},
        {_id: 10, exerciseName: "Core Press", equipment: 4, muscles: 11, baseSets: 1, baseReps: 3, baseTime: 12, exerciseClass : "strength"},
        {_id: 11, exerciseName: "Curl", equipment: [4, 8, 13, 25, 59, 82], muscles: 8, baseSets: 3, baseReps: 10, baseTime: 1, exerciseClass : "strength"},
        {_id: 12, exerciseName: "Lunge", equipment: [0, 13, 25, 59, 82, 86, 12], muscles: [1, 2, 3, 12], baseSets: 3, baseReps: 10, baseTime: 1, exerciseClass : "strength"},
        {_id: 13, exerciseName: "Deadlift", equipment: [13, 59], muscles: [1, 2, 10], baseSets: 3, baseReps: 8, baseTime: 1, exerciseClass : "strength"},
        {_id: 14, exerciseName: "Dip", equipment: [13, 59], muscles: [4, 7], baseSets: 3, baseReps: 20, baseTime: 1, exerciseClass : "strength"},
        {_id: 15, exerciseName: "Figure Skating", equipment: 41, muscles: [1, 3, 11], baseSets: 1, baseReps: 1, baseTime: 1200, exerciseClass : "cardio"},
        {_id: 16, exerciseName: "Free Skating", equipment: 41, muscles: [1, 3], baseSets: 1, baseReps: 1, baseTime: 1200, exerciseClass : "cardio"},
        {_id: 17, exerciseName: "Hammer Curl", equipment: [4, 25], muscles: 8, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 18, exerciseName: "Hamstring Curl", equipment: [19, 57, 86], muscles: 2, baseSets: 3, baseReps: 15, baseTime: 1, exerciseClass : "strength"},
        {_id: 19, exerciseName: "Hamstring Pull-in", equipment: [31, 82], muscles: 2, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 20, exerciseName: "Handball", equipment: 65, muscles: 0, baseSets: 1, baseReps: 1, baseTime: 600, exerciseClass : "cardio"},
        {_id: 21, exerciseName: "Hockey", equipment: 41, muscles: [1, 3], baseSets: 1, baseReps: 1, baseTime: 2400, exerciseClass : "cardio"},
        {_id: 22, exerciseName: "Jogging", equipment: [0, 45, 81, 87], muscles: [1, 2, 3], baseSets: 1, baseReps: 1800, baseTime: 1, exerciseClass : "cardio"},
        {_id: 23, exerciseName: "Kettlebell Swing", equipment: 48, muscles: 2, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 24, exerciseName: "Knee Drive", equipment: 82, muscles: 1, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 25, exerciseName: "Kneeling One Arm Row", equipment: 25, muscles: [5, 7], baseSets: 3, baseReps: 15, baseTime: 1, exerciseClass : "strength"},
        {_id: 26, exerciseName: "Lateral Raise", equipment: [4, 25], muscles: 6, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 28, exerciseName: "Lat Pulldown", equipment: [4, 51, 32, 85], muscles: 13, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 29, exerciseName: "Leg Extension", equipment: [19, 54], muscles: 1, baseSets: 3, baseReps: 20, baseTime: 1, exerciseClass : "strength"},
        {_id: 30, exerciseName: "Low-to-High Chop", equipment: 19, muscles: 0, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 32, exerciseName: "Lying Fly", equipment: 25, muscles: 4, baseSets: 3, baseReps: 10, baseTime: 1, exerciseClass : "strength"},
        {_id: 33, exerciseName: "Military Press", equipment: [13, 60], muscles: 6, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 34, exerciseName: "Overhead Press", equipment: [35, 48, 59, 62], muscles: 6, baseSets: 3, baseReps: 6, baseTime: 1, exerciseClass : "strength"},
        {_id: 35, exerciseName: "Pectoral Fly", equipment: [63, 64], muscles: 4, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 36, exerciseName: "Plank", equipment: [0, 12, 86], muscles: [6, 7, 9], baseSets: 1, baseReps: 1, baseTime: 60, exerciseClass : "cardio"},
        {_id: 37, exerciseName: "Plank Row", equipment: 37, muscles: 5, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 38, exerciseName: "Pullover", equipment: 13, muscles: 13, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 39, exerciseName: "Pull-Through", equipment: 19, muscles: 0, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 40, exerciseName: "Pull-up", equipment: 63, muscles: [5, 7, 10, 13], baseSets: 2, baseReps: 5, baseTime: 1, exerciseClass : "strength"},
        {_id: 42, exerciseName: "Pushup", equipment: [0, 59, 82, 86], muscles: [4, 7, 8], baseSets: 3, baseReps: 10, baseTime: 1, exerciseClass : "strength"},
        {_id: 43, exerciseName: "Racquetball", equipment: 65, muscles: 0, baseSets: 1, baseReps: 1, baseTime: 1800, exerciseClass : "cardio"},
        {_id: 44, exerciseName: "Rotational Chop", equipment: 4, muscles: 0, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 45, exerciseName: "Row", equipment: [4, 13, 19, 34, 37, 58, 69, 82, 83], muscles: 5, baseSets: 3, baseReps: 10, baseTime: 1, exerciseClass : "strength"},
        {_id: 46, exerciseName: "Shoulder Press", equipment: [25, 59, 35], muscles: 6, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 47, exerciseName: "Shrug", equipment: 13, muscles: 6, baseSets: 3, baseReps: 15, baseTime: 1, exerciseClass : "strength"},
        {_id: 48, exerciseName: "Side Bend", equipment: 19, muscles: 11, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 49, exerciseName: "Sit-up", equipment: [0, 43, 59], muscles: 11, baseSets: 4, baseReps: 15, baseTime: 1, exerciseClass : "strength"},
        {_id: 50, exerciseName: "Snatch", equipment: [13, 48], muscles: 6, baseSets: 5, baseReps: 5, baseTime: 1, exerciseClass : "strength"},
        {_id: 51, exerciseName: "Sprinting", equipment: [0, 45, 81], muscles: [1, 2, 3, 12], baseSets: 1, baseReps: 1, baseTime: 60, exerciseClass : "cardio"},
        {_id: 52, exerciseName: "Squat", equipment: [0, 12, 13, 19, 33, 36, 38, 48, 59, 73, 74, 86], muscles: [1, 2, 3, 12], baseSets: 5, baseReps: 5, baseTime: 1, exerciseClass : "strength"},
        {_id: 53, exerciseName: "Squat Thrust", equipment: 37, muscles: [1, 2, 3, 12], baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 54, exerciseName: "Stationary Lunge", equipment: 25, muscles: [2, 12], baseSets: 3, baseReps: 8, baseTime: 1, exerciseClass : "strength"},
        {_id: 55, exerciseName: "Toe Raise", equipment: 25, muscles: 3, baseSets: 1, baseReps: 2, baseTime: 20, exerciseClass : "strength"},
        {_id: 56, exerciseName: "Tricep Dip", equipment: [10, 86], muscles: 7, baseSets: 3, baseReps: 30, baseTime: 1, exerciseClass : "strength"},
        {_id: 57, exerciseName: "Tricep Extension", equipment: [4, 13, 59], muscles: 7, baseSets: 3, baseReps: 8, baseTime: 1, exerciseClass : "strength"},
        {_id: 59, exerciseName: "Triceps Kickback", equipment: 25, muscles: 7, baseSets: 3, baseReps: 8, baseTime: 1, exerciseClass : "strength"},
        {_id: 60, exerciseName: "Turkish Get-up", equipment: 48, muscles: 6, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 61, exerciseName: "Twist", equipment: 59, muscles: 11, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 62, exerciseName: "Upright Row", equipment: 25, muscles: 5, baseSets: 3, baseReps: 10, baseTime: 1, exerciseClass : "strength"},
        {_id: 63, exerciseName: "V-up", equipment: [0, 12, 59, 86], muscles: 1, baseSets: 2, baseReps: 10, baseTime: 1, exerciseClass : "strength"},
        {_id: 64, exerciseName: "Windmill", equipment: [12], muscles: 11, baseSets: 3, baseReps: 12, baseTime: 1, exerciseClass : "strength"},
        {_id: 65, exerciseName: "Cardio-Row", equipment: 70, muscles: [1, 5, 10], baseSets: 1, baseReps: 1, baseTime: 60, exerciseClass : "cardio"},
        {_id: 66, exerciseName: "Agility Drill", equipment: [5,6], muscles: 3, baseSets: 1, baseReps: 1, baseTime: 60, exerciseClass : "cardio"},
        {_id: 67, exerciseName: "Jump Rope", equipment: 47, muscles: [1, 2, 3], baseSets: 1, baseReps: 1, baseTime: 60, exerciseClass : "cardio"},
        {_id: 68, exerciseName: "Rope Swing", equipment: 39, muscles: [6, 7], baseSets: 1, baseReps: 1, baseTime: 120, exerciseClass : "cardio"},
        {_id: 69, exerciseName: "Bike", equipment: [7, 66, 72, 84, 88 ], muscles: [1, 2, 3, 12], baseSets: 1, baseReps: 1, baseTime: 3600, exerciseClass : "cardio"},
        {_id: 70, exerciseName: "Elliptical", equipment: 27, muscles: [1, 2, 3, 12], baseSets: 1, baseReps: 1, baseTime: 2400, exerciseClass : "cardio"},
        {_id: 71, exerciseName: "Swimming", equipment: 50, muscles: [2, 3, 4,5, 6, 8], baseSets: 1, baseReps: 1, baseTime: 2400, exerciseClass : "cardio"},
        {_id: 72, exerciseName: "Diving", equipment: 24, muscles: 0, baseSets: 1, baseReps: 1, baseTime: 1800, exerciseClass : "cardio"},
        {_id: 73, exerciseName: "Climbing", equipment: [17, 52, 79], muscles: [1, 3, 6, 7, 8, 9, 13], baseSets: 1, baseReps: 1, baseTime: 2400, exerciseClass : "cardio"},
        {_id: 74, exerciseName: "Stretch", equipment:[0, 28, 29, 76, 77], muscles: 0, baseSets: 1, baseReps: 1, baseTime: 600, exerciseClass : "cardio"},
        {_id: 76, exerciseName: "Basketball", equipment: 14, muscles: [1,2,3,12], baseSets: 1, baseReps: 1, baseTime: 1800, exerciseClass : "cardio"}
] );
} catch (e) {
    print(e);
}
// workouts insert
try {
db.workouts.insert( [
        {_id:1, exercises:[2,3], workoutName:"back explosion", exerciseClass: 'strength'},
        {_id:2, exercises:[7,47], workoutName:"bicep attack", exerciseClass: 'strength'},
        {_id:3, exercises:[24, 25], workoutName:"heart attack", exerciseClass: 'strength'},
        {_id:4, exercises:[56, 4], workoutName:"squatalot", exerciseClass: 'strength'}
] ) ;
} catch (e) {
    print(e);
}
// muscles insert
try {
db.muscles.insert( [
        {_id: 1, muscleName: "Miscellaneous"},
        {_id: 2, muscleName: "Quadriceps"},
        {_id: 3, muscleName: "Hamstrings"},
        {_id: 4, muscleName: "Calves"},
        {_id: 5, muscleName: "Chest"},
        {_id: 6, muscleName: "Back"},
        {_id: 7, muscleName: "Shoulders"},
        {_id: 8, muscleName: "Triceps"},
        {_id: 9, muscleName: "Biceps"},
        {_id: 10, muscleName: "Forearms"},
        {_id: 11, muscleName: "Trapezius"},
        {_id: 12, muscleName: "Abs"},
        {_id: 13, muscleName: "Glutes"},
        {_id: 14, muscleName: "Lats"}
] );
} catch (e) {
    print(e);
}
// equipment
try {
db.equipment.insert( [
        {_id: 1, equipmentName: "No Equipment Required" },
        {_id: 2, equipmentName: "Ab Crunch Ball" },
        {_id: 3, equipmentName: "Ab Crunch Bench" },
        {_id: 4, equipmentName: "Abdominal Machine"  },
        {_id: 5, equipmentName: "Adjustable Cable"  },
        {_id: 6, equipmentName: "Agility Dots"  },
        {_id: 7, equipmentName: "Agility Ladder"  },
        {_id: 8, equipmentName: "Arc trainer"  },
        {_id: 9, equipmentName: "Arm Curl"  },
        {_id: 10, equipmentName: "Arm Extension"  },
        {_id: 11, equipmentName: "Assisted Pull Up Machine"},
        {_id: 12, equipmentName: "Back Extension"  },
        {_id: 13, equipmentName: "Balance Disk"  },
        {_id: 14, equipmentName: "Barbells"   },
        {_id: 15, equipmentName: "Basketball Courts"  },
        {_id: 16, equipmentName: "Bench Press"  },
        {_id: 17, equipmentName: "Bosu Leg Lift" },
        {_id: 18, equipmentName: "Bouldering Rock Wall" },
        {_id: 19, equipmentName: "Box Jump"  },
        {_id: 20, equipmentName: "Cable column"  },
        {_id: 21, equipmentName: "Calf Raise"  },
        {_id: 22, equipmentName: "Chest Press"  },
        {_id: 23, equipmentName: "Cybex Back Extension" },
        {_id: 24, equipmentName: "Dip Machine"  },
        {_id: 25, equipmentName: "Diving Pool"  },
        {_id: 26, equipmentName: "Dumbbells"   },
        {_id: 27, equipmentName: "Eagle Prone Leg Curl"},
        {_id: 28, equipmentName: "Elliptical"   },
        {_id: 29, equipmentName: "Flexibility Anterior"  },
        {_id: 30, equipmentName: "Flexibility posterior"  },
        {_id: 31, equipmentName: "Free Motion Chest" },
        {_id: 32, equipmentName: "Free Motion Hamstring" },
        {_id: 33, equipmentName: "Free Motion Lat" },
        {_id: 34, equipmentName: "Free Motion Quad" },
        {_id: 35, equipmentName: "Free Motion Row" },
        {_id: 36, equipmentName: "Free Motion Shoulder" },
        {_id: 37, equipmentName: "Free Motion Squat" },
        {_id: 38, equipmentName: "GripR Sandbags"  },
        {_id: 39, equipmentName: "Ground Base Squat" },
        {_id: 40, equipmentName: "Heavy Bag"  },
        {_id: 41, equipmentName: "Heavy Rope"  },
        {_id: 42, equipmentName: "Ice Rink"  },
        {_id: 43, equipmentName: "Incline Press"  },
        {_id: 44, equipmentName: "Incline Sit-up"  },
        {_id: 45, equipmentName: "Indoor Soccer Field" },
        {_id: 46, equipmentName: "Indoor track"  },
        {_id: 47, equipmentName: "Jump Rope"  },
        {_id: 48, equipmentName: "Jump Rope"  },
        {_id: 49, equipmentName: "Kettle Balls"  },
        {_id: 50, equipmentName: "Kneeling Leg Curl" },
        {_id: 51, equipmentName: "Lap Pool"  },
        {_id: 52, equipmentName: "Lat Pulldown"  },
        {_id: 53, equipmentName: "Lead Rock Wall" },
        {_id: 54, equipmentName: "Leg Curl"  },
        {_id: 55, equipmentName: "Leg Extension"  },
        {_id: 56, equipmentName: "Leg Press"  },
        {_id: 57, equipmentName: "Light Bag"  },
        {_id: 58, equipmentName: "Lower Back Machine" },
        {_id: 59, equipmentName: "Low Row"  },
        {_id: 60, equipmentName: "Medicine Ball"  },
        {_id: 61, equipmentName: "Military Bench"  },
        {_id: 62, equipmentName: "Multi Hip"  },
        {_id: 63, equipmentName: "Overhead Press"  },
        {_id: 64, equipmentName: "Pectoral Flys"  },
        {_id: 65, equipmentName: "Pectoral Machine"  },
        {_id: 66, equipmentName: "Racquetball Court"  },
        {_id: 67, equipmentName: "Recumbent bike"  },
        {_id: 68, equipmentName: "Rotary Calf"  },
        {_id: 69, equipmentName: "Rotary Torso"  },
        {_id: 70, equipmentName: "Row"   },
        {_id: 71, equipmentName: "Row Machine"  },
        {_id: 72, equipmentName: "Seated Leg Curl" },
        {_id: 73, equipmentName: "Spin Bikes"  },
        {_id: 74, equipmentName: "Squat Press"  },
        {_id: 75, equipmentName: "Squat Rack"  },
        {_id: 76, equipmentName: "Stair Climbers"  },
        {_id: 77, equipmentName: "Stretch station"  },
        {_id: 78, equipmentName: "Stretch Trainer"  },
        {_id: 79, equipmentName: "Tennis Court"  },
        {_id: 80, equipmentName: "Top Rope Rock Wall"},
        {_id: 81, equipmentName: "Total Abdominal"  },
        {_id: 82, equipmentName: "Tread Mill"  },
        {_id: 83, equipmentName: "TRX"   },
        {_id: 84, equipmentName: "Upper Back Machine" },
        {_id: 85, equipmentName: "Upright bike"  },
        {_id: 86, equipmentName: "Vertical Traction"  },
        {_id: 87, equipmentName: "Yoga Ball"  },
        {_id: 88, equipmentName: "Free Run"},
        {_id: 89, equipmentName: "Bike"}
] );
} catch (e) {
    print(e);
}

// print all collections
show collections
