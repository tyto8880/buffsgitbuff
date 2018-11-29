from app import database as db
import unittest

class databaseTester(unittest.TestCase):
	
	def testCreateUser(self):
		db.deleteUser("Bobb")
		#create user
		ret = db.createUser("Bobb","bob@gmail.com","password")
		self.assertTrue(ret)
		#create existing user
		ret = db.createUser("Bobb","bobby@gmail.com","mops")
		self.assertFalse(ret)
	
	def testGetUserInfo(self):
		db.createUser("Bobb","bob@gmail.com","password")#create a user/make sure this one exists
		#try to get this user's info
		ret = db.getUserInfo("Bobb")
		self.assertIsNotNone(ret)
		self.assertEqual(ret["username"],"Bobb")
		self.assertEqual(ret["email"],"bob@gmail.com")
		
		#try to get a user that doesn't exist
		ret = db.getUserInfo("cthulu ftagn")
		self.assertIsNone(ret)
	
	def testValidateUser(self):
		db.createUser("Bobb","bob@gmail.com","password")
		#validate existing user with correct password
		ret = db.validateUser("Bobb","password")
		self.assertTrue(ret)
		
		#validate existing user with incorrect password
		ret = db.validateUser("Bobb","assbutt")
		self.assertFalse(ret)
		
		#validate nonexistent user
		ret = db.validateUser("cthulu ftagn","maximus")
		self.assertFalse(ret)
	
	def testDeleteuser(self):
		db.createUser("Bobb","bob@gmail.com","password")
		#delete existing user
		ret = db.deleteUser("Bobb")
		self.assertTrue(ret)
		#make sure Bobb isn't in the database
		ret = db.getUserInfo("Bobb")
		self.assertIsNone(ret)

		#delete nonexistent user
		ret = db.deleteUser("cthulu ftagn")
		self.assertFalse(ret)

# Main: Run Test Cases
if __name__ == '__main__':
    unittest.main()