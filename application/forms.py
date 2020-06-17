from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextField, SelectField, TextAreaField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError,Email
from application.models import User, Customer, Account

class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=8)],render_kw={"placeholder": "Username"})
	password = PasswordField("Password", validators=[DataRequired()],render_kw={"placeholder": "Password"})
	submit = SubmitField("Login")

	def validate_password(self, password):
		if len(password.data) != 10:
			raise ValidationError("Password length must be 10 characters!!!")
		
		upper=False
		digit=False
		for ch in password.data:
			if ch.isupper():
				upper=True
			if ch.isdigit():
				digit=True
		
		if not upper:
			raise ValidationError("Password should contain atleast 1 upper case alphabet!!!")
		
		if not digit:
			raise ValidationError("Password should contain atleast 1 digit case alphabet!!!")
		
		if password.data.isalpha():
			raise ValidationError("Password should contain atleast 1 special character!!!")

class CustomerDetailsForm(FlaskForm):
	ssn_id = IntegerField("Customer SSN Id",validators=[DataRequired()]) 
	cust_id = IntegerField("Customer ID",validators=[DataRequired()])
	cust_name = StringField("Customer Name",validators=[DataRequired(),Length(max=30)])
	address = TextField("Address",validators=[DataRequired(),Length(max=30)])
	contact = IntegerField("Contact",validators=[DataRequired()])
	cust_age = IntegerField("Age",validators=[DataRequired()])
	state = SelectField("State",validators=[DataRequired()],choices=[("Gujarat","Gujarat"),("Maharashtra","Maharashtra")])
	city = SelectField("City",validators=[DataRequired()],choices=[("Ahmedabad","Ahemdabad"),("Pune","Pune")])
	submit = SubmitField("Submit")
	
	def validate_ssnid(self,ssn_id):
		customer = Customer.filter_by(ssn=ssn_id).first()
		if customer:
			raise ValidationError("SSN Id is already in use. Pick another one.")
		if len(ssn_id.data)>10:
			raise ValidationError("SSN Id should be not more than 9 digit numeric.")
		
	def validate_age(self,cust_age):
		if cust_age.data>120:
			raise ValidationError("Age should be not more than 3 digit numeric or more than 120.")
		if cust_age.data<0:
			raise ValidationError("Age should be a positive integer number.")

class ContactForm(FlaskForm):
	fullName = TextField('First Name',validators=[DataRequired()])
	email = TextField('E-mail',validators=[DataRequired(), Email()])
	subject = TextField('Subject',validators=[DataRequired()])
	message = TextAreaField('Message',validators=[DataRequired()])
	submit = SubmitField('Send')

class SearchCustomerForm(FlaskForm):
	ssn_id = IntegerField("Customer SSN Id", default=0, validators=[]) 
	cust_id = IntegerField("Customer ID", default=0, validators=[])
	submit = SubmitField("Submit")
	
	def validate_ssnid(self,ssn_id):
		if ssn_id.data>999999999:
			raise ValidationError("SSN Id should be not more than 9 digit numeric.")

class CustomerConfirmationForm(FlaskForm):
	confirm = BooleanField("Yes")
	cust_id = IntegerField("Enter the Customer ID again to confirm!!!", default=0, validators=[])
	submit = SubmitField("Confirm")

class AccountDetailsForm(FlaskForm):
	acc_no = IntegerField("Account Number", default=Account.generate_acc_no(), validators=[DataRequired()]) 
	acc_balance = FloatField("Account Balance", default=1000, validators=[DataRequired()])
	acc_type = SelectField("Account Type", validators=[DataRequired()], choices=[('S', "Savings"),('C', "Current")])
	cust_id = IntegerField("Customer ID",validators=[DataRequired()])
	submit = SubmitField("Create Account")
	
	def validate_balance(self,balance):
		if balance < 100:
			raise ValidationError("The minimum balance to open a new account is Rs. 1000")


	def validate_cust_id(self,cust_id):
		customer = Customer.query.filter_by(cust_id=cust_id)
		if not customer:
			raise ValidationError("Enter a valid customer ID.")

class SearchAccountForm(FlaskForm):
	acc_no = IntegerField("Account Number", default=0, validators=[])
	cust_id = IntegerField("Customer ID", default=0, validators=[])
	acc_type = SelectField("Account Type", validators=[], choices=[('S', "Savings"),('C', "Current")])
	submit = SubmitField("Submit")

class AccountConfirmationForm(FlaskForm):
	confirm = BooleanField("Yes")
	acc_no = IntegerField("Enter the Account No. again to confirm!!!", validators=[])
	submit = SubmitField("Confirm")


class DepositMoneyForm(FlaskForm):
	depositAmount = FloatField("Deposit Amount", validators=[DataRequired()])
	submit = SubmitField("Deposit")

	def validate_depositAmount(self, depositAmount):
		if depositAmount < 0:
			raise ValidationError("Wrong Input!!!")

class WithdrawMoneyForm(FlaskForm):
	withdrawAmount = FloatField("Withdraw Amount", validators=[DataRequired()])
	submit = SubmitField("Withdraw")

class TransferMoneyForm(FlaskForm):
	amount = FloatField("Amount", validators=[DataRequired()])
	from_acc = SelectField("From Account Type", validators=[DataRequired()], default='S', choices=[('S', "Savings"),('C', "Current")])
	to_acc = SelectField("To Account Type", validators=[DataRequired()], default='C', choices=[('S', "Savings"),('C', "Current")])
	submit = SubmitField("Transfer")