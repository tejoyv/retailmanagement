from application import app, db, bcrypt, mail
from application.forms import LoginForm, CustomerDetailsForm, AccountDetailsForm, ContactForm, SearchCustomerForm, CustomerConfirmationForm, SearchAccountForm, AccountConfirmationForm
from application.models import User, Customer, Account
from flask import render_template, redirect, flash, url_for, session, request
from flask_mail import Message
from application.utils import mail_send, searchCustomer, searchAccount

@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
def home():
	if request.method == "POST":
		print("hello")
		fullname = request.form.get('fullname')
		email = request.form.get('email')
		message = request.form.get('message')

		value = mail_send(fullname,email,message)
		return value
	else:
		return render_template("home.html",title="Moody Bank",role=session.get('ROLE'))


@app.route("/login", methods=['GET', 'POST'])
def login():
	if session.get('USER_ID'):
		return redirect(url_for('home'))
	else:
		form = LoginForm()
		if form.validate_on_submit():
			user = User.query.filter_by(user_id=form.username.data).first()
			if bcrypt.check_password_hash(user.password, form.password.data):
				flash("Successfully logged in!!!", category="success")
				session['USER_ID'] = user.user_id
				session['ROLE'] = user.role
				return redirect(url_for('home'))
			else:
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
	    if form.validate_on_submit():
	        customer = Customer(ssn=form.ssn_id.data,cust_id=form.cust_id.data,cust_name=form.cust_name.data,
	                           cust_address=form.address.data,cust_contact = form.contact.data,cust_age=form.cust_age.data,cust_state=form.state.data,cust_city=form.city.data)
	        db.session.add(customer)
	        db.session.commit()
	        return redirect("/create_customer")
	    return render_template("create_customer.html",form=form, title="Create Customer")


#============================================Misc Functions=======================================#
def show_account_details(account, delete=False):
	form_conf = AccountConfirmationForm()
	if delete:
		if form_conf.validate_on_submit():
			print(form_conf.confirm.data)
			if form_conf.confirm.data == True and form_conf.acc_no.data == account.acc_no:
				db.session.delete(account)
				db.session.commit()
				flash("Customer Deleted!!!")
				return redirect('home')
	return render_template('show_account_details.html', account=account, delete=delete, title="Show Account Details", form=form_conf)


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
			flash("Customer Successfully Deleted!!!")
			return redirect(url_for('home'))
		else:
			flash("Wrong input data!!!")
			return redirect(url_for('home'))
	return render_template('delete_confirmation_form.html', title="Confirm Delete", form=form)



#============================================Update Customer=======================================#
@app.route("/update_customer_details/<int:cust_id>", methods=['GET', 'POST'])
def update_customer_details(cust_id):
	customer = Customer.query.filter_by(cust_id=cust_id).first()
	form = CustomerDetailsForm()
	if form.validate_on_submit():
		customer.cust_name = form.cust_name.data
		customer.address = form.address.data
		customer.contact = form.contact.data
		customer.cust_age = form.cust_age.data
		db.session.commit()
		flash("Customer Details are updated!!!")
		return redirect(url_for('home'))
	return render_template('update_customer_details.html', title="Update Details", form=form, customer=customer)


@app.route("/update_customer/<int:cust_id>", methods=['GET', 'POST'])
def update_customer(cust_id):
	customer = Customer.query.filter_by(cust_id=cust_id).first()
	form = CustomerConfirmationForm()
	if form.validate_on_submit():
		if form.confirm.data and form.cust_id.data == cust_id:
			return redirect(url_for('update_customer_details', cust_id=cust_id))
		else:
			flash("Wrong input data!!!")
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
				return "Customer not found..."
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


#============================================View All Accounts=======================================#
@app.route("/view_accounts_status", methods=['GET', 'POST'])
def view_accounts_status():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
		page = request.args.get('page', 1, type=int)
		accounts = Account.query.order_by(Account.acc_no).paginate(page=page, per_page=10)
		return render_template("view_accounts_status.html", accounts=accounts, title="View All Accounts")

#============================================Create New Account=======================================#
@app.route("/create_account",methods=["GET","POST"])
def create_account():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
	    form = AccountDetailsForm()
	    if form.validate_on_submit():
	        account = Account(acc_no=form.acc_no.data, acc_balance=form.acc_balance.data, acc_type=form.acc_type.data, cust_id=form.cust_id.data)
	        db.session.add(account)
	        db.session.commit()
	        return redirect("/create_account")
	    return render_template("create_account.html",form=form, title="Create Customer")

#============================================Delete Account=======================================#
@app.route("/delete_account",methods=["GET","POST"])
def delete_account():
	form = SearchAccountForm()
	if form.validate_on_submit():
		account = searchAccount(acc_no=form.acc_no.data, cust_id=form.cust_id.data, acc_type=form.acc_type.data)
		if account == None:
			return "Account not found!!!"
		else:
			return show_account_details(account, delete=True)
	return render_template('delete_account.html', form=form, title="Delete Account")

#============================================Search Account=======================================#
@app.route("/search_account",methods=["GET","POST"])
def search_account():
	form = SearchAccountForm()
	if form.validate_on_submit():
		account = searchAccount(acc_no=form.acc_no.data, cust_id=form.cust_id.data, acc_type=form.acc_type.data)
		if account == None:
			return "Account not found!!!"
		else:
			return show_account_details(account)
	return render_template('search_account.html', form=form, title="Search Account")


#============================================Deposite Money=======================================#


@app.route("/logout", methods=['GET', 'POST'])
def logout():
	session['USER_ID'] = None
	session['ROLE'] = None
	return redirect(url_for('home'))