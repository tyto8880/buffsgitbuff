# buffsgitbuff
Buffs git Buff is a workout website that allows users to create workouts with their preferences on the fly with our workout generation algorithm. So sit back, relax and get Buff!

---
To run the automated tests:
1. Ensure all of the relevant Python libraries are installed using any Python package manager. Here is the list of necessary libraries:
	1. pymongo
	2. numpy
	3. scipy
	4. flask
	5. passlib
	6. unittest
2. Ensure that mongodb is installed (https://docs.mongodb.com/manual/installation/)
3. Create a directory for the database to exist outside of the git repository directory. This can be done with the command (from the git repo) `mkdir ../database`.
4. Start the mongo server with the command `mongod -dbpath ../<database directory>`
5. Now that the database server is running, the database must itself be populated. This can be done by (from the main git repo directory) running the following command: `mongo < createDatabase.js`
6. Now that the database is both running and populated, the tests themselves can be run with the following command: `python3 databaseTests.py`
