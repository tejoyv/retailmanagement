from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError,Email
from application.models import User,Customer

class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=8)])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Submit")

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

class CreateCustomerForm(FlaskForm):
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

class SearchUserForm(FlaskForm):
	ssn_id = IntegerField("Customer SSN Id", default=0, validators=[]) 
	cust_id = IntegerField("Customer ID", default=0, validators=[])
	submit = SubmitField("Submit")
	
	def validate_ssnid(self,ssn_id):
		if ssn_id.data>999999999:
			raise ValidationError("SSN Id should be not more than 9 digit numeric.")

class ConfirmationForm(FlaskForm):
	confirm = BooleanField("Are you sure??", default=True, validators=[])
	cust_id = IntegerField("Enter the Customer ID again to confirm!!!", validators=[])
	submit = SubmitField("Confirm")
