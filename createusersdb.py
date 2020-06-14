from application import db, bcrypt
from application.models import User
import random as rd

'''
There will be 5 users with random access as teller and acc_exec
'''

idStart = 0
role=["acc_exec", "teller"]
for _ in range(5):
	user_id = "User"+str(idStart+11111)
	password = "User@"+str(idStart+11111)
	password = bcrypt.generate_password_hash(password).decode('utf-8')
	user = User(user_id=user_id, password=password, role=role[rd.randint(0, 1)])
	db.session.add(user)
	db.session.commit()
	idStart += 11111
	print("user added", user)

users = User.query.all()
for user in users:
	print(user)
print(len(users))

