from application import db

class User(db.Model):
	id = db.Column(db.String(20), primary_key=True, nullable=False)
	password = db.Column(db.String(10), nullable=False)
	role = db.Column(db.String(10), nullable=False)

class Customer(db.Model):
	ssn = db.Column(db.Integer, primary_key=True)
	cust_id = db.Column(db.Integer, unique=True, nullable=False)
	cust_name = db.Column(db.String(20), nullable=False)
	cust_address = db.Column(db.Text, nullable=False)
	cust_contact = db.Column(db.Integer, nullable=True)
	accounts = db.relationship('Account', backref='Owner', lazy=True)


class Account(db.Model):
	acc_no = db.Column(db.Integer, primary_key=True)
	acc_balance = db.Column(db.Float, nullable=False)
	cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'), nullable=False)
	transactions = db.relationship('Transactions', backref='accounts', lazy=True)


class Transactions(db.Model):
	transaction_id = db.Column(db.Integer, primary_key=True)
	action = db.Column(db.String(10), nullable=False)
	acc_no = db.Column(db.Integer, db.ForeignKey('account.acc_no'), nullable=False)
	