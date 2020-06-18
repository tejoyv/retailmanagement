from application import app, db, bcrypt, mail
from application.forms import LoginForm, CustomerDetailsForm, AccountDetailsForm, ContactForm, SearchCustomerForm, CustomerConfirmationForm, SearchAccountForm, AccountConfirmationForm, DepositMoneyForm, WithdrawMoneyForm, TransferMoneyForm, PrintStatementForm
from application.models import User, Customer, Account
from flask import render_template, redirect, flash, url_for, session, request
from flask_mail import Message
from application.utils import mail_send, searchCustomer, searchAccount, depositMoney, withdrawMoney, transferMoney

@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
def home():
	if request.method == "POST":
		fullname = request.form.get('fullname')
		email = request.form.get('email')
		message = request.form.get('message')

		value = mail_send(fullname,email,message)
		return value
	else:
		return render_template("home.html",title="Moody Bank")


@app.route("/login", methods=['GET', 'POST'])
def login():
	if session.get('USER_ID'):
		return redirect(url_for('home'))
	else:
		form = LoginForm()
		if form.validate_on_submit():
			user = User.query.filter_by(user_id=form.username.data).first()
			if  user and bcrypt.check_password_hash(user.password, form.password.data):
				flash("Successfully logged in!!!", category="success")
				session['USER_ID'] = user.user_id
				session['ROLE'] = user.role
				return redirect(url_for('dashboard'))
			elif  user and not bcrypt.check_password_hash(user.password, form.password.data):
				flash("Wrong password entered!!!", category="danger")
			else:	
				flash("Wrong username entered!!!", category="danger")
		return render_template("login.html", title="Login", form=form)
  
#============================================Account executive routes=======================================#
 
#============================================Create Customer=======================================#
@app.route("/create_customer",methods=["GET","POST"])
def create_customer():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
	    form = CustomerDetailsForm()
	    form.cust_id.data = Customer.generate_cust_id()
	    if form.validate_on_submit():
	        customer = Customer(ssn=form.ssn_id.data,cust_id=form.cust_id.data,cust_name=form.cust_name.data, cust_address=form.address.data, cust_contact = form.contact.data,cust_age=form.cust_age.data,cust_state=form.state.data,cust_city=form.city.data)
	        db.session.add(customer)
	        db.session.commit()
	        flash("Customer Successfully Created!!!", category="success")
	        return redirect(url_for('home'))
	    return render_template("create_customer.html",form=form, title="Create Customer")


#============================================Delete Customer=======================================#
@app.route("/delete_customer/<int:cust_id>", methods=['GET', 'POST'])
def delete_customer(cust_id):
	customer = Customer.query.filter_by(cust_id=cust_id).first()
	form = CustomerConfirmationForm()
	if form.validate_on_submit():
		if form.confirm.data and form.cust_id.data == cust_id:
			for account in customer.accounts:
				db.session.delete(account)
				db.session.commit()
			for transaction in customer.transactions:
				db.session.delete(transaction)
				db.session.commit()
			db.session.delete(customer)
			db.session.commit()
			flash("Customer Successfully Deleted!!!", category="success")
			return redirect(url_for('home'))
		elif (not form.confirm.data) or (form.cust_id.data != cust_id):
			flash("Wrong input data!!!", category="danger")
			return redirect(url_for('home'))
	return render_template('delete_confirmation_form.html', title="Confirm Delete", form=form)



#============================================Update Customer=======================================#
@app.route("/update_customer_details/<int:cust_id>", methods=['GET', 'POST'])
def update_customer_details(cust_id):
	form = CustomerDetailsForm()
	customer = searchCustomer(cust_id=cust_id)
	form.ssn_id.data = customer.ssn
	form.cust_id.data = customer.cust_id
	if form.validate_on_submit():
		customer.cust_name = form.cust_name.data
		customer.cust_address = form.address.data
		customer.cust_contact = form.contact.data
		customer.cust_age = form.cust_age.data
		db.session.commit()
		flash("Customer Details are updated!!!", category="success")
		return redirect(url_for('home'))
	return render_template('update_customer_details.html', cust_id=cust_id, title="Update Customer Details", form=form)

@app.route("/update_customer/<int:cust_id>", methods=['GET', 'POST'])
def update_customer(cust_id):
	customer = Customer.query.filter_by(cust_id=cust_id).first()
	form = CustomerConfirmationForm()
	if form.validate_on_submit():
		if form.confirm.data and form.cust_id.data == cust_id:
			return redirect(url_for('update_customer_details', cust_id=cust_id))
			return render_template('update_customer_details.html', title="Update Details", form=form, customer=customer)
		else:
			flash("Wrong input data!!!", category="danger")
			return redirect(url_for('home'))
	return render_template('update_confirmation_form.html', title="Confirm Delete", form=form)

#============================================Search Customer=======================================#
@app.route('/search_customer', methods=['GET', 'POST'])
def search_customer():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
		form = SearchCustomerForm()
		if form.validate_on_submit():
			customer = searchCustomer(ssn=form.ssn_id.data, cust_id=form.cust_id.data)
			if customer == None:
				flash("Customer not found...", category="danger")
				return redirect(url_for('home'))
			else:
				return render_template('show_customer_details.html', customer=customer, title="Show Customer Details")
		else:
			return render_template('search_customer.html', form=form, title="Search Customer")

#============================================View All Customers=======================================#
@app.route("/view_customers_status", methods=['GET', 'POST'])
def view_customers_status():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
		page = request.args.get('page', 1, type=int)
		customers = Customer.query.order_by(Customer.cust_id).paginate(page=page, per_page=10)
		return render_template("view_customers_status.html", customers=customers, title="View All Customer")


@app.route("/show_customer_details/<int:cust_id>")
def show_customer_details(cust_id):
	customer = Customer.query.filter_by(cust_id=cust_id).first()
	if customer == None:
		flash("Customer not found...", category="danger")
		return redirect(url_for('home'))
	else:
		return render_template('show_customer_details.html', customer=customer, title="Show Customer Details")

#============================================View All Accounts=======================================#
@app.route("/view_accounts_status", methods=['GET', 'POST'])
def view_accounts_status():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
		page = request.args.get('page', 1, type=int)
		accounts = Account.query.order_by(Account.acc_no).paginate(page=page, per_page=10)
		return render_template("view_accounts_status.html", accounts=accounts, title="View All Accounts")

@app.route("/show_account_details/<int:acc_no>")
def show_account_details(acc_no):
	account = Account.query.filter_by(acc_no=acc_no).first()
	if account == None:
		flash("Account not found...", category="danger")
		return redirect(url_for('home'))
	else:
		return render_template('show_account_details.html', account=account, title="Show Account Details")

#============================================Create New Account=======================================#
@app.route("/create_account",methods=["GET","POST"])
def create_account():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
	    form = AccountDetailsForm()
	    form.acc_no.data = Account.generate_acc_no()
	    if form.validate_on_submit():
	        account = Account(acc_no=form.acc_no.data, acc_balance=form.acc_balance.data, acc_type=form.acc_type.data, cust_id=form.cust_id.data)
	        db.session.add(account)
	        db.session.commit()
	        flash("Account Successfully Created!!!", category="success")
	        return redirect(url_for('home'))
	    return render_template("create_account.html",form=form, title="Create Customer")

#============================================Delete Account=======================================#
@app.route("/delete_account/<int:acc_no>",methods=["GET","POST"])
def delete_account(acc_no):
	account = Account.query.filter_by(acc_no=acc_no).first()
	form = AccountConfirmationForm()
	if form.validate_on_submit():
		if form.confirm.data and form.acc_no.data == acc_no:
			db.session.delete(account)
			db.session.commit()
			flash("Account Successfully Deleted!!!", category="success")
			return redirect(url_for('home'))
		elif (not form.confirm.data) or (form.acc_no.data != acc_no):
			flash("Wrong input data!!!", category="danger")
			return redirect(url_for('home'))
	return render_template('delete_confirmation_form.html', title="Confirm Delete", form=form)

#============================================Search Account=======================================#
@app.route("/search_account",methods=["GET","POST"])
def search_account():
	form = SearchAccountForm()
	if form.validate_on_submit():
		account = searchAccount(acc_no=form.acc_no.data, cust_id=form.cust_id.data, acc_type=form.acc_type.data)
		if account == None:
			flash("Acount not found...", category="danger")
			return redirect(url_for('home'))
		else:
			return render_template('show_account_details.html', account=account, title="Show Account Details")
	return render_template('search_account.html', form=form, title="Search Account")


#============================================Deposite Money=======================================#
@app.route("/deposit/<int:acc_no>",methods=["GET","POST"])
def deposit(acc_no):
	form = DepositMoneyForm()
	account = searchAccount(acc_no=acc_no)
	if form.validate_on_submit():
		result = depositMoney(depositAmount=form.depositAmount.data, acc_no=acc_no)
		if result == "Success":
			flash("Amount Successfully Deposited...", category="success")
			return redirect(url_for('show_account_details', acc_no=account.acc_no))
		else:
			flash("Amount Not Deposited...", category="danger")
			return redirect(url_for('show_account_details', acc_no=account.acc_no))
	return render_template("deposit.html",title="Deposit Money", account=account, form=form)


#============================================Withdraw Money=======================================#
@app.route("/withdraw/<int:acc_no>",methods=["GET","POST"])
def withdraw(acc_no):
	form = WithdrawMoneyForm()
	account = Account.query.filter_by(acc_no=acc_no).first()
	if form.validate_on_submit():
		result = withdrawMoney(withdrawAmount=form.withdrawAmount.data, acc_no=acc_no)
		if result == "Success":
			flash("Amount Successfully withdrawn...", category="success")
			return redirect(url_for('show_account_details', acc_no=account.acc_no))
		else:
			flash("Amount Not Withdrawn...", category="danger")
			return redirect(url_for('show_account_details', acc_no=account.acc_no))
	return render_template("withdraw.html",title="Withdraw Money", account=account, form=form)

#============================================Transfer Money=======================================#
@app.route("/transfer/<int:acc_no>",methods=["GET","POST"])
def transfer(acc_no):
	form = TransferMoneyForm()
	account = searchAccount(acc_no=acc_no)
	if form.validate_on_submit():
		print(form.amount.data, account.cust_id, form.from_acc.data, form.to_acc.data)
		result = transferMoney(amount=form.amount.data, cust_id=account.cust_id, from_acc=form.from_acc.data, to_acc=form.to_acc.data)
		if result == "Success":
			flash("Amount Successfully Transfered...", category="success")
			return redirect(url_for('show_account_details', acc_no=account.acc_no))
		else:
			flash("Amount Not Transfered...", category="danger")
			return redirect(url_for('show_account_details', acc_no=account.acc_no))
	return render_template("transfer.html",title="Transfer Money", account=account, form=form)

#============================================Account Statement=======================================#
@app.route("/acc_statement/<int:acc_no>",methods=["GET","POST"])
def acc_statement(acc_no):
	form = PrintStatementForm()
	account = Account.query.filter_by(acc_no=acc_no).first()
	customer = Customer.query.filter_by(cust_id=account.cust_id).first()
	if form.validate_on_submit():
		if form.choice.data == 'LT':
			transactions = customer.transactions
			transactions = transactions[-form.no_of_transactions.data:]
			return render_template('show_transactions.html', transactions=transactions, title="Account Statement", account=account)
		elif form.choice.data == 'BD':
			transactions = customer.transactions
			statement_transactions = []
			for transaction in transactions:
				if transaction.transaction_date >= form.from_date.data and transaction.transaction_date <= form.to_date.data:
					statement_transactions.append(transaction)
			return render_template('show_transactions.html', transactions=statement_transactions, title="Account Statement", account=account)
	return render_template("acc_statement.html",title="Account Statement", form=form)


@app.route("/dashboard")
def dashboard():
	customers = len(Customer.query.all())
	account = len(Account.query.all())
	return render_template("dashboard.html",title="Dashboard",customers=customers,account=account)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
	session['USER_ID'] = None
	session['ROLE'] = None
	return redirect(url_for('home'))

