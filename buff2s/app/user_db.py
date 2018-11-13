import pymongo
from passlib.hash import pbkdf2_sha256 as pl

client = pymongo.MongoClient("localhost",27017)
db = client.Buffs

"""
uname is the user's username
pwd is the user's password (not sure if we'd pass this or just the password hash to the server)
"""
def get_user_info(uname,pwd):
	info = db.Users.find({"username":uname}
	#make sure the user exists
	if(len(info) == 0):
		return False
	#now verify their password
	pwh = info["passwordHash"]
	if not pl.verify(pwd,pwh):
		return False
	return info

"""
may need to also pass other settings here
"""
def create_user(uname,pwd):
	if(len(db.Users.find({"username":uname})) != 0):
		#a user with this username already exists
		return False
	
	pwh = pl.hash(pwd)#salt included in the hash
	db.Users.insertOne({"username":uname,
						"pwh":pwh,
						"favoriteExercises":[],
						"cardio":-1,
						"strength":-1})
	return True
