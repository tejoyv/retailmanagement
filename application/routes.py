from application import app, db, bcrypt, mail
from application.forms import LoginForm, CustomerDetailsForm, AccountDetailsForm, ContactForm, SearchUserForm, UserConfirmationForm, SearchAccountForm, AccountConfirmationForm
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
def show_customer_details(customer, delete=False, update=False):
	form_conf = UserConfirmationForm()
	if update:
		if form_conf.validate_on_submit():
			if form_conf.confirm.data == True and form_conf.cust_id.data == customer.cust_id:
				if session.get('ROLE') != "acc_exec":
					return "Action Not Allowed"
				else:
					form = CustomerDetailsForm()
					if form.validate_on_submit():
						customer.cust_name = form.cust_name.data
						customer.cust_address=form.address.data
						customer.cust_contact = form.contact.data
						customer.cust_age = form.cust_age.data
						customer.cust_state = form.state.data
						customer.cust_city = form.city.data
						db.session.commit()
						flash("Customer Details Updated")
						return redirect('home')
					return render_template('update_customer_details.html', form=form, title="Update Customer Details")

	elif delete:
		if form_conf.validate_on_submit():
			print(form_conf.confirm.data)
			if form_conf.confirm.data == True and form_conf.cust_id.data == customer.cust_id:
				db.session.delete(customer)
				db.session.commit()
				flash("Customer Deleted!!!")
				return redirect('home')
	return render_template('show_customer_details.html', customer=customer, delete=delete, update=update, title="Show Customer Details", form=form_conf)

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
@app.route("/delete_customer", methods=['GET', 'POST'])
def delete_customer():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
		form = SearchUserForm()
		if form.validate_on_submit():
			customer = searchCustomer(ssn=form.ssn_id.data, cust_id=form.cust_id.data)
			if customer == None:
				return "Customer not found..."
			else:
				return show_customer_details(customer, delete=True, update=False)
	return render_template('delete_customer.html', form=form, title="Delete Customer")


#============================================Update Customer=======================================#
@app.route("/update_customer", methods=['GET', 'POST'])
def update_customer():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
		form = SearchUserForm()
		if form.validate_on_submit():
			customer = searchCustomer(ssn=form.ssn_id.data, cust_id=form.cust_id.data)
			if customer == None:
				return "Customer not found..."
			else:
				return show_customer_details(customer, delete=False, update=True)
		else:
			return render_template('update_customer.html', form=form, title="Update Customer")

#============================================Search Customer=======================================#
@app.route('/search_customer', methods=['GET', 'POST'])
def search_customer():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
		form = SearchUserForm()
		if form.validate_on_submit():
			customer = searchCustomer(ssn=form.ssn_id.data, cust_id=form.cust_id.data)
			if customer == None:
				return "Customer not found..."
			else:
				return show_customer_details(customer, delete=False, update=False)
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



@app.route("/logout", methods=['GET', 'POST'])
def logout():
	session['USER_ID'] = None
	session['ROLE'] = None
	return redirect(url_for('home'))

@app.route("/deposit",methods=["GET","POST"])
def deposit():
	return render_template("deposit.html",title="Deposit Money")

@app.route("/withdraw",methods=["GET","POST"])
def withdraw():
	return render_template("withdraw.html",title="Withdraw Money")

@app.route("/transfer",methods=["GET","POST"])
def transfer():
	return render_template("transfer.html",title="Transfer Money")

@app.route("/acc_statement",methods=["GET","POST"])
def acc_statement():
	return render_template("acc_statement.html",title="Account Statement")