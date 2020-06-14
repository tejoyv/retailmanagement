from application import app, db, bcrypt
from application.forms import LoginForm, RegisterationForm
from application.models import User, Customer, Account
from flask import render_template, redirect, flash, url_for, session, request


@app.route("/")
def home():
	return render_template("home.html", title="Home", role=session.get('ROLE'))


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
				return redirect('home.html', title="Home", role=session.get('ROLE'))
			else:
				flash("Wrong password entered!!!", category="danger")
		else:
			flash("Wrong username entered!!!", category="danger")
		return render_template("login.html", title="Login", form=form)
  
 
@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        customer = Customer(ssn=form.ssn_id.data,cust_name=form.cust_name.data,
                           cust_age=form.cust_age.data,cust_address=form.address.data,cust_state=form.state.data,cust_city=form.city.data)
        db.session.add(customer)
        db.session.commit()
        return redirect("/register")
    return render_template("register.html",customer=customer,form=form)


@app.route("/view_customers_status", methods=['GET', 'POST'])
def viewCustomersStatus():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
		page = request.args.get('page', 1, type=int)
		customers = Customer.query.order_by(Customer.cust_id).paginate(page=page, per_page=10)
		return render_template('view_status.html', customers=customers)


@app.route("/view_accounts_status", methods=['GET', 'POST'])
def viewAccountsStatus():
	if session.get('ROLE') != "acc_exec":
		return "Action Not Allowed"
	else:
		page = request.args.get('page', 1, type=int)
		customers = Account.query.order_by(Account.acc_id).paginate(page=page, per_page=10)
		return render_template('view_status.html', accounts=accounts)
