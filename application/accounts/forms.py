from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField, FloatField, RadioField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from application.models import Customer
from datetime import datetime as dt



class AccountDetailsForm(FlaskForm):
	acc_no = IntegerField("Account Number", validators=[DataRequired()]) 
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
		if self.depositAmount.data < 0:
			raise ValidationError("Wrong Input!!!")

class WithdrawMoneyForm(FlaskForm):
	withdrawAmount = FloatField("Withdraw Amount", validators=[DataRequired()])
	submit = SubmitField("Withdraw")

	def validate_withdrawAmount(self, depositAmount):
		if self.withdrawAmount.data < 0:
			raise ValidationError("Wrong Input!!!")

class TransferMoneyForm(FlaskForm):
	amount = FloatField("Amount", validators=[DataRequired()])
	from_acc = SelectField("From Account Type", validators=[DataRequired()], default='S', choices=[('S', "Savings"),('C', "Current")])
	to_acc = SelectField("To Account Type", validators=[DataRequired()], default='C', choices=[('S', "Savings"),('C', "Current")])
	submit = SubmitField("Transfer")

class PrintStatementForm(FlaskForm):
	choice = RadioField("Get Transactions By :", validators=[DataRequired()], choices=[('LT','Last Transactions'), ('BD', 'Between Dates')], default='BD')
	no_of_transactions = IntegerField("How Many Transactions?", validators=[], default=10)
	from_date = DateTimeField("From Date (YYYY-MM-DD)",default=dt.now().date(), validators=[])
	to_date = DateTimeField("To Date (YYYY-MM-DD)",default=dt.now().date(), validators=[])
	submit = SubmitField("Show Statement")
