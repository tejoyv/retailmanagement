from application import db, bcrypt
from application.models import Customer, Account
import random as rd

accountnumber = rd.randint(10000000, 11111111)

customers = Customer.query.all()
for customer in customers:
	account1 = Account(acc_no=accountnumber+1, acc_balance=float(rd.randint(1000, 10000)), acc_type='S', cust_id=customer.cust_id)
	accountnumber+=1
	print(account1)
	db.session.add(account1)
	db.session.commit()
	account2 = Account(acc_no=accountnumber+1, acc_balance=float(rd.randint(1000, 10000)), acc_type='C', cust_id=customer.cust_id)
	accountnumber+=1
	print(account2)
	db.session.add(account2)
	db.session.commit()

accounts = Account.query.all()
for account in accounts:
	print(account)