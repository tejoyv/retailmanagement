from application import app,db
from flask import render_template,request,redirect,flash,url_for
from application.models import Customer,User
from application.forms import RegisterationForm,UserForm


@app.route("/")
@app.route("/login")
def index():
    return render_template("login.html", title="Login")

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

