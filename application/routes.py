from application import app, db, bcrypt, mail
from application.forms import LoginForm, RegisterationForm, ContactForm
from application.models import User, Customer, Account
from flask import render_template, redirect, flash, url_for, session, request
from flask_mail import Message
from application.utils import mail_send

@app.route("/",methods=["GET","POST"])
def home():
	'''<<<<<<< HEAD
	msg=""
	form = ContactForm()
	if form.validate_on_submit():	
		msg = Message("Hello",sender="moodybanktcs@gmail.com",recipients=["tejoyv@gmail.com"])
		msg.body = "Hello Flask message sent from Flask-Mail"
		mail.send(msg)
		return "Sent"
	return render_template("home.html",title="Home", form=form, role=session.get('ROLE'))
	======='''
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
	#>>>>>>> 82558e6cb291c7d99e6a72df573b85bf13f739a2


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
  
 
@app.route("/register",methods=["GET","POST"])
def register():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
	    form = RegisterationForm()
	    if form.validate_on_submit():
	        customer = Customer(ssn=form.ssn_id.data,cust_id=form.cust_id.data,cust_name=form.cust_name.data,
	                           cust_address=form.address.data,cust_contact = form.contact.data,cust_age=form.cust_age.data,cust_state=form.state.data,cust_city=form.city.data)
	        db.session.add(customer)
	        db.session.commit()
	        return redirect("/register")
	    return render_template("register.html",form=form)


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