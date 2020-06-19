from application import db
from application.customers.forms import CustomerDetailsForm, SearchCustomerForm, CustomerConfirmationForm
from application.models import Customer
from flask import render_template, redirect, flash, url_for, session, Blueprint
from application.utils import searchCustomer


customers = Blueprint('customers', __name__)

#============================================Create Customer=======================================#
@customers.route("/create_customer",methods=["GET","POST"])
def create_customer():
	if session.get('ROLE') != "acc_exec":
		flash("Action Not Allowed", category="danger")
		return redirect('main.home')
	else:
	    form = CustomerDetailsForm()
	    form.choice.data = 'C'
	    form.cust_id.data = Customer.generate_cust_id()
	    if form.validate_on_submit():
	        customer = Customer(ssn=form.ssn_id.data,cust_id=form.cust_id.data,cust_name=form.cust_name.data, cust_address=form.address.data, cust_contact = form.contact.data,cust_age=form.cust_age.data,cust_state=form.state.data,cust_city=form.city.data)
	        db.session.add(customer)
	        db.session.commit()
	        flash("Customer Successfully Created!!!", category="success")
	        return redirect(url_for('main.home'))
	    return render_template("customers/create_customer.html",form=form, title="Create Customer")


#============================================Delete Customer=======================================#
@customers.route("/delete_customer/<int:cust_id>", methods=['GET', 'POST'])
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
			flash("Customer Successfully Deleted!!!", category="success")
			return redirect(url_for('main.home'))
		elif (not form.confirm.data) or (form.cust_id.data != cust_id):
			flash("Wrong input data!!!", category="danger")
			return redirect(url_for('main.home'))
	return render_template('customers/delete_confirmation_form.html', title="Confirm Delete", form=form, cust_id=cust_id)



#============================================Update Customer=======================================#
@customers.route("/update_customer_details/<int:cust_id>", methods=['GET', 'POST'])
def update_customer_details(cust_id):
	form = CustomerDetailsForm()
	customer = searchCustomer(cust_id=cust_id)
	form.ssn_id.data = customer.ssn
	form.cust_id.data = customer.cust_id
	form.choice.data = 'U'
	if form.validate_on_submit():
		customer.cust_name = form.cust_name.data
		customer.cust_address = form.address.data
		customer.cust_contact = form.contact.data
		customer.cust_age = form.cust_age.data
		customer.cust_state = form.state.data
		customer.cust_city = form.city.data
		db.session.commit()
		flash("Customer Details are updated!!!", category="success")
		return redirect(url_for('main.home'))
	return render_template('customers/update_customer_details.html', cust_id=cust_id, title="Update Customer Details", form=form)

@customers.route("/update_customer/<int:cust_id>", methods=['GET', 'POST'])
def update_customer(cust_id):
	customer = Customer.query.filter_by(cust_id=cust_id).first()
	form = CustomerConfirmationForm()
	if form.validate_on_submit():
		if form.confirm.data and form.cust_id.data == cust_id:
			return redirect(url_for('customers.update_customer_details', cust_id=cust_id))
			return render_template('customers/update_customer_details.html', title="Update Details", form=form, customer=customer)
		else:
			flash("Wrong input data!!!", category="danger")
			return redirect(url_for('main.home'))
	return render_template('customers/update_confirmation_form.html', title="Confirm Delete", form=form, cust_id=cust_id)

#============================================Search Customer=======================================#
@customers.route('/search_customer', methods=['GET', 'POST'])
def search_customer():
	if session.get('ROLE') != "acc_exec":
		flash("Action Not Allowed", category="danger")
		return redirect('main.home')
	else:
		form = SearchCustomerForm()
		if form.validate_on_submit():
			customer = searchCustomer(ssn=form.ssn_id.data, cust_id=form.cust_id.data)
			if customer == None:
				flash("Customer not found...", category="danger")
				return redirect(url_for('main.home'))
			else:
				return render_template('customers/show_customer_details.html', customer=customer, title="Show Customer Details")
		else:
			return render_template('customers/search_customer.html', form=form, title="Search Customer")

