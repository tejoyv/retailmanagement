from application import bcrypt
from application.main.forms import LoginForm
from application.models import User, Customer, Account
from flask import render_template, redirect, flash, url_for, session, request, Blueprint
from application.utils import mail_send


main = Blueprint('main', __name__)

@main.route("/",methods=["GET","POST"])
@main.route("/home",methods=["GET","POST"])
def home():
	if request.method == "POST":
		fullname = request.form.get('fullname')
		email = request.form.get('email')
		message = request.form.get('message')
		value = mail_send(fullname,email,message)
		flash("Mail Successfully Sent", category="success")
		return redirect(url_for('main.home'))
	else:
		return render_template("main/home.html",title="Moody Bank")


@main.route("/login", methods=['GET', 'POST'])
def login():
	if session.get('USER_ID'):
		return redirect(url_for('main.home'))
	else:
		form = LoginForm()
		if form.validate_on_submit():
			user = User.query.filter_by(user_id=form.username.data).first()
			if  user and bcrypt.check_password_hash(user.password, form.password.data):
				flash("Successfully logged in!!!", category="success")
				session['USER_ID'] = user.user_id
				session['ROLE'] = user.role
				return redirect(url_for('main.dashboard'))
			elif  user and not bcrypt.check_password_hash(user.password, form.password.data):
				flash("Wrong password entered!!!", category="danger")
			else:	
				flash("Wrong username entered!!!", category="danger")
		return render_template("main/login.html", title="Login", form=form)
  
@main.route("/logout")
def logout():
	session['USER_ID'] = None
	session['ROLE'] = None
	return redirect(url_for('main.home'))


@main.route("/dashboard")
def dashboard():
	customers = len(Customer.query.all())
	account = len(Account.query.all())
	return render_template("main/dashboard.html",title="Dashboard",customers=customers,account=account)

 
#============================================View All Accounts=======================================#
@main.route("/view_accounts_status", methods=['GET', 'POST'])
def view_accounts_status():
	if session.get('ROLE') != "acc_exec":
		flash("Action Not Allowed", category="danger")
		return redirect('main.home')
	else:
		page = request.args.get('page', 1, type=int)
		accounts = Account.query.order_by(Account.acc_no).paginate(page=page, per_page=10)
		return render_template("accounts/view_accounts_status.html", accounts=accounts, title="View All Accounts")

@main.route("/show_account_details/<int:acc_no>")
def show_account_details(acc_no):
	account = Account.query.filter_by(acc_no=acc_no).first()
	if account == None:
		flash("Account not found...", category="danger")
		return redirect(url_for('main.home'))
	else:
		return render_template('accounts/show_account_details.html', account=account, title="Show Account Details")


#============================================View All Customers=======================================#
@main.route("/view_customers_status", methods=['GET', 'POST'])
def view_customers_status():
	if session.get('ROLE') != "acc_exec":
		flash("Action Not Allowed", category="danger")
		return redirect('main.home')
	else:
		page = request.args.get('page', 1, type=int)
		customers = Customer.query.order_by(Customer.cust_id).paginate(page=page, per_page=10)
		return render_template("customers/view_customers_status.html", customers=customers, title="View All Customer")


@main.route("/show_customer_details/<int:cust_id>")
def show_customer_details(cust_id):
	customer = Customer.query.filter_by(cust_id=cust_id).first()
	if customer == None:
		flash("Customer not found...", category="danger")
		return redirect(url_for('main.home'))
	else:
		return render_template('customers/show_customer_details.html', customer=customer, title="Show Customer Details")

