from application import db,mail
from application.models import Customer, Account, Transaction
from flask_mail import Message

def searchCustomer(ssn=None, cust_id=None):
	if ssn != None:
		customer = Customer.query.filter_by(ssn=ssn).first()
		if customer:
			return customer
		else:
			return None
	elif cust_id != None:
		customer = Customer.query.filter_by(cust_id=cust_id).first()
		if customer:	
			return customer
		else:
			return None
	else:
		return None

def searchAccount(acc_no=None, cust_id=None, acc_type='S'):
	if acc_no != None:
		account = Account.query.filter_by(acc_no=acc_no).first()
		if account:
			return account
		else:
			return None
	elif cust_id != None:
		customer = Customer.query.filter_by(cust_id=cust_id).first()
		if customer:
			for account in customer.accounts:
				if account.acc_type == acc_type:
					return account
		else:
			return None
	else:
		return None

def depositMoney(depositAmount, acc_no=None, cust_id=None, acc_type='S'):
	account = searchAccount(acc_no=acc_no, cust_id=cust_id, acc_type=acc_type)
	if account != None:
		account.acc_balance += depositAmount
		db.session.commit()
		num_transactions = len(Transaction.query.all())
		transaction = Transaction(transaction_id=num_transactions+1, transaction_amount=depositAmount, from_acc=acc_type, to_acc=acc_type, action="Deposit", cust_id=account.cust_id)
		db.session.add(transaction)
		db.session.commit()
		return "Success"
	else:
		return "Failure"

def withdrawMoney(withdrawAmount, acc_no=None, cust_id=None, acc_type='S'):
	account = searchAccount(acc_no=acc_no, cust_id=cust_id, acc_type=acc_type)
	if account != None:
		account.acc_balance += withdrawAmount
		db.session.commit()
		num_transactions = len(Transaction.query.all())
		transaction = Transaction(transaction_id=num_transactions+1, transaction_amount=withdrawAmount, from_acc=acc_type, to_acc=acc_type, action="Withdraw", cust_id=account.cust_id)
		db.session.add(transaction)
		db.session.commit()
		return "Success"
	else:
		return "Failure"

def transferMoney(amount, cust_id, from_acc, to_acc):
	fromAccount = searchAccount(cust_id=cust_id, acc_type=from_acc)
	toAccount = searchAccount(cust_id=cust_id, acc_type=to_acc)
	if fromAccount==None or toAccount==None:
		return "Failure"
	else:
		num_transactions = len(Transaction.query.all())
		fromAccount.acc_balance -= amount
		toAccount.acc_balance += amount
		db.session.commit()
		transaction = Transaction(transaction_id=num_transactions+1, transaction_amount=amount, from_acc=from_acc, to_acc=to_acc, action="Transfer", cust_id=fromAccount.cust_id)
		db.session.add(transaction)
		db.session.commit()
		return "Success"

def mail_send(fullname,email,message):
	msg = Message("Hello",sender="moodybanktcs@gmail.com",recipients=[email])
	msg.body = message
	mail.send(msg)
	return "Mail Sent"	