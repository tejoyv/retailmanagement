from application import db, bcrypt
from application.models import Customer, Transaction
import application.utils as ut
import random as rd

tid = rd.randint(55555555, 99999999)

customers = Customer.query.all()
i=1
for customer in customers:
	print("customer no. ", i)
	result = ut.depositMoney(float(rd.randint(1000, 10000)), cust_id=customer.cust_id)
	print(result)
	result = ut.withdrawMoney(float(rd.randint(1000, 10000)), cust_id=customer.cust_id)
	print(result)
	result = ut.depositMoney(float(rd.randint(1000, 10000)), cust_id=customer.cust_id, acc_type='C')
	print(result)
	result = ut.withdrawMoney(float(rd.randint(1000, 10000)), cust_id=customer.cust_id, acc_type='C')
	print(result)
	print("1 deposite 1 withdraw in both accounts")
	result = ut.depositMoney(float(rd.randint(1000, 10000)), cust_id=customer.cust_id)
	print(result)
	result = ut.withdrawMoney(float(rd.randint(1000, 10000)), cust_id=customer.cust_id)
	print(result)
	result = ut.depositMoney(float(rd.randint(1000, 10000)), cust_id=customer.cust_id, acc_type='C')
	print(result)
	result = ut.withdrawMoney(float(rd.randint(1000, 10000)), cust_id=customer.cust_id, acc_type='C')
	print(result)
	print("2 deposite 2 withdraw in both accounts")
	result = ut.transferMoney(float(rd.randint(1000, 10000)), cust_id=customer.cust_id, from_acc='S', to_acc='C')
	print(result)
	result = ut.transferMoney(float(rd.randint(1000, 10000)), cust_id=customer.cust_id, from_acc='S', to_acc='C')
	print(result)
	result = ut.transferMoney(float(rd.randint(1000, 10000)), cust_id=customer.cust_id, from_acc='C', to_acc='S')
	print(result)
	result = ut.transferMoney(float(rd.randint(1000, 10000)), cust_id=customer.cust_id, from_acc='C', to_acc='S')
	print(result)
	print("2 transfer form savings to current 2 transfer from current to savings")
	i+=1

print("total transactions added :", len(Transaction.query.all()))