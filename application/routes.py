from application import app
from flask import render_template

@app.route("/")
@app.route("/login")
def index():
    return render_template("login.html", title="Login")