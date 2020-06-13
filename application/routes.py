from application import app, db, bcrypt
from application.forms import LoginForm
from application.models import User
from flask import render_template, redirect, flash, url_for, session

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