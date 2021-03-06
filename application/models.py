from application import db
from datetime import datetime as d

class User(db.Model):
	user_id = db.Column(db.String(20), primary_key=True, nullable=False)
	password = db.Column(db.String(10), nullable=False)
	role = db.Column(db.String(10), nullable=False)
	
	def __repr__(self):
		return f"User('{self.user_id}', '{self.role}')"


class Customer(db.Model):
	ssn = db.Column(db.Integer, primary_key=True)
	cust_id = db.Column(db.Integer, unique=True, nullable=False)
	cust_name = db.Column(db.String(20), nullable=False)
	cust_address = db.Column(db.Text, nullable=False)
	cust_contact = db.Column(db.Integer,nullable=False)
	cust_age = db.Column(db.Integer, nullable=False)
	cust_state = db.Column(db.String(20),nullable=False)
	cust_city = db.Column(db.String(30),nullable=False)
	accounts = db.relationship('Account', backref='Owner', lazy=True)
	transactions = db.relationship('Transaction', backref='Owner', lazy=True)

	@staticmethod
	def generate_cust_id():
		first_cust_id = Customer.query.first().cust_id
		tot_accounts = len(Customer.query.all())
		return (first_cust_id + tot_accounts + 1)

	def __repr__(self):
		return f"Customer('{self.cust_id}', '{self.cust_name}')"

class Account(db.Model):
	acc_no = db.Column(db.Integer, primary_key=True)
	acc_balance = db.Column(db.Float, nullable=False)
	acc_type = db.Column(db.String(1), nullable=False)
	acc_createDate = db.Column(db.DateTime, nullable=False, default=d.today())
	cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'), nullable=False)
	
	@staticmethod
	def generate_acc_no():
		first_acc_no = Account.query.first().acc_no
		tot_accounts = len(Account.query.all())
		return (first_acc_no + tot_accounts + 2)

	def __repr__(self):
		return f"Account('{self.acc_no}', '{self.acc_type}', '{self.acc_balance}', '{self.acc_createDate}')"

class Transaction(db.Model):
	transaction_id = db.Column(db.Integer, primary_key=True)
	transaction_date = db.Column(db.DateTime, nullable=False, default=d.today())
	transaction_amount = db.Column(db.Float, nullable=False)
	from_acc = db.Column(db.String(1), nullable=False)
	to_acc = db.Column(db.String(1), nullable=False)
	action = db.Column(db.String(10), nullable=False)
	cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'), nullable=False)
	
	def __repr__(self):
		return f"Transaction('{self.transaction_id}', '{self.transaction_date}', '{self.transaction_amount}', '{self.from_acc}', '{self.to_acc}')"
