from application import app, db, bcrypt, mail
from application.forms import LoginForm, CreateCustomerForm, ContactForm, SearchUserForm
from application.models import User, Customer, Account
from flask import render_template, redirect, flash, url_for, session, request
from flask_mail import Message
from application.utils import mail_send, searchCustomer, searchAccount

@app.route("/",methods=["GET","POST"])
def home():
	form = ContactForm()
	if request.method == "POST":
		print("hello")
		fullname = request.form.get('fullname')
		email = request.form.get('email')
		message = request.form.get('message')

		value = mail_send(fullname,email,message)
		return value
	else:
		return render_template("home.html", title="Moody Bank", role=session.get('ROLE'), form=form)


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
	    form = CreateCustomerForm()
	    if form.validate_on_submit():
	        customer = Customer(ssn=form.ssn_id.data,cust_id=form.cust_id.data,cust_name=form.cust_name.data,
	                           cust_address=form.address.data,cust_contact = form.contact.data,cust_age=form.cust_age.data,cust_state=form.state.data,cust_city=form.city.data)
	        db.session.add(customer)
	        db.session.commit()
	        return redirect("/create_customer")
	    return render_template("create_customer.html",form=form)
#============================================Misc Functions=======================================#
def show_customer_details(customer, delete=False, update=False):
	return render_template('show_customer_details.html', customer=customer, delete=delete, update=update)




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
		else:
			return render_template('delete_customer.html', form=form)


#============================================Delete Customer=======================================#
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
			return render_template('update_customer.html', form=form)

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
			return render_template('search_customer.html', form=form)

@app.route("/view_customers_status", methods=['GET', 'POST'])
def view_customers_status():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
		page = request.args.get('page', 1, type=int)
		customers = Customer.query.order_by(Customer.cust_id).paginate(page=page, per_page=10)
		return render_template("view_customers_status.html", customers=customers)


@app.route("/view_accounts_status", methods=['GET', 'POST'])
def view_accounts_status():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
		page = request.args.get('page', 1, type=int)
		accounts = Account.query.order_by(Account.acc_no).paginate(page=page, per_page=10)
		return render_template("view_accounts_status.html", accounts=accounts)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
	session['USER_ID'] = None
	session['ROLE'] = None
	return redirect(url_for('home'))