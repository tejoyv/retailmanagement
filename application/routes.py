from application import app
from application.forms import LoginForm
from flask import render_template, redirect, flash

@app.route("/")
def home():
	return render_template("home.html", title="Home")

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm
	if validate_on_submit():
		flash("Successfully logged in!!!", category="success")
		return redirect('home.html', title="Home")
	else:
		return render_template("login.html", title="Login", form=form)