from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextField, SelectField, TextAreaField, BooleanField, FloatField, RadioField, DateTimeField
from wtforms.validators import DataRequired, Length, ValidationError,Email
from application.models import User, Customer, Account
from datetime import datetime as dt

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
	cust_id = IntegerField("Customer ID", validators=[DataRequired()])
	cust_name = StringField("Customer Name",validators=[DataRequired(),Length(max=30)])
	address = TextField("Address",validators=[DataRequired(),Length(max=30)])
	contact = IntegerField("Contact",validators=[DataRequired()])
	cust_age = IntegerField("Age",validators=[DataRequired()])
	state = SelectField("State",validators=[DataRequired()],choices=[("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry")])
	city = SelectField("City",validators=[DataRequired()],choices=[('Mumbai', 'Mumbai'), ('Delhi', 'Delhi'), ('Kolkata', 'Kolkata'), ('Chennai', 'Chennai'), ('Bengalūru', 'Bengalūru'), ('Hyderabad', 'Hyderabad'), ('Ahmadābād', 'Ahmadābād'), ('Hāora', 'Hāora'), ('Pune', 'Pune'), ('Sūrat', 'Sūrat'), ('Mardānpur', 'Mardānpur'), ('Rāmpura', 'Rāmpura'), ('Lucknow', 'Lucknow'), ('Nāra', 'Nāra'), ('Patna', 'Patna'), ('Indore', 'Indore'), ('Vadodara', 'Vadodara'), ('Bhopal', 'Bhopal'), ('Coimbatore', 'Coimbatore'), ('Ludhiāna', 'Ludhiāna'), ('Āgra', 'Āgra'), ('Kalyān', 'Kalyān'), ('Vishākhapatnam', 'Vishākhapatnam'), ('Kochi', 'Kochi'), ('Nāsik', 'Nāsik'), ('Meerut', 'Meerut'), ('Farīdābād', 'Farīdābād'), ('Vārānasi', 'Vārānasi'), ('Ghāziābād', 'Ghāziābād'), ('Āsansol', 'Āsansol'), ('Jamshedpur', 'Jamshedpur'), ('Madurai', 'Madurai'), ('Jabalpur', 'Jabalpur'), ('Rājkot', 'Rājkot'), ('Dhanbād', 'Dhanbād'), ('Amritsar', 'Amritsar'), ('Warangal', 'Warangal'), ('Allahābād', 'Allahābād'), ('Srīnagar', 'Srīnagar'), ('Aurangābād', 'Aurangābād'), ('Bhilai', 'Bhilai'), ('Solāpur', 'Solāpur'), ('Ranchi', 'Ranchi'), ('Jodhpur', 'Jodhpur'), ('Guwāhāti', 'Guwāhāti'), ('Chandigarh', 'Chandigarh'), ('Gwalior', 'Gwalior'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Tiruchchirāppalli', 'Tiruchchirāppalli'), ('Hubli', 'Hubli'), ('Mysore', 'Mysore'), ('Raipur', 'Raipur'), ('Salem', 'Salem'), ('Bhubaneshwar', 'Bhubaneshwar'), ('Kota', 'Kota'), ('Jhānsi', 'Jhānsi'), ('Bareilly', 'Bareilly'), ('Alīgarh', 'Alīgarh'), ('Bhiwandi', 'Bhiwandi'), ('Jammu', 'Jammu'), ('Morādābād', 'Morādābād'), ('Mangalore', 'Mangalore'), ('Kolhāpur', 'Kolhāpur'), ('Amrāvati', 'Amrāvati'), ('Dehra Dūn', 'Dehra Dūn'), ('Mālegaon Camp', 'Mālegaon Camp'), ('Nellore', 'Nellore'), ('Gopālpur', 'Gopālpur'), ('Shimoga', 'Shimoga'), ('Tiruppūr', 'Tiruppūr'), ('Raurkela', 'Raurkela'), ('Nānded', 'Nānded'), ('Belgaum', 'Belgaum'), ('Sāngli', 'Sāngli'), ('Chānda', 'Chānda'), ('Ajmer', 'Ajmer'), ('Cuttack', 'Cuttack'), ('Bīkaner', 'Bīkaner'), ('Bhāvnagar', 'Bhāvnagar'), ('Hisar', 'Hisar'), ('Bilāspur', 'Bilāspur'), ('Tirunelveli', 'Tirunelveli'), ('Guntūr', 'Guntūr'), ('Shiliguri', 'Shiliguri'), ('Ujjain', 'Ujjain'), ('Davangere', 'Davangere'), ('Akola', 'Akola'), ('Sahāranpur', 'Sahāranpur'), ('Gulbarga', 'Gulbarga'), ('Bhātpāra', 'Bhātpāra'), ('Dhūlia', 'Dhūlia'), ('Udaipur', 'Udaipur'), ('Bellary', 'Bellary'), ('Tuticorin', 'Tuticorin'), ('Kurnool', 'Kurnool'), ('Gaya', 'Gaya'), ('Sīkar', 'Sīkar'), ('Tumkūr', 'Tumkūr'), ('Kollam', 'Kollam'), ('Ahmadnagar', 'Ahmadnagar'), ('Bhīlwāra', 'Bhīlwāra'), ('Nizāmābād', 'Nizāmābād'), ('Parbhani', 'Parbhani'), ('Shillong', 'Shillong'), ('Lātūr', 'Lātūr'), ('Rājapālaiyam', 'Rājapālaiyam'), ('Bhāgalpur', 'Bhāgalpur'), ('Muzaffarnagar', 'Muzaffarnagar'), ('Muzaffarpur', 'Muzaffarpur'), ('Mathura', 'Mathura'), ('Patiāla', 'Patiāla'), ('Saugor', 'Saugor'), ('Brahmapur', 'Brahmapur'), ('Shāhbāzpur', 'Shāhbāzpur'), ('New Delhi', 'New Delhi'), ('Rohtak', 'Rohtak'), ('Samlaipādar', 'Samlaipādar'), ('Ratlām', 'Ratlām'), ('Fīrozābād', 'Fīrozābād'), ('Rājahmundry', 'Rājahmundry'), ('Barddhamān', 'Barddhamān'), ('Bīdar', 'Bīdar'), ('Bamanpurī', 'Bamanpurī'), ('Kākināda', 'Kākināda'), ('Pānīpat', 'Pānīpat'), ('Khammam', 'Khammam'), ('Bhuj', 'Bhuj'), ('Karīmnagar', 'Karīmnagar'), ('Tirupati', 'Tirupati'), ('Hospet', 'Hospet'), ('Chikka Mandya', 'Chikka Mandya'), ('Alwar', 'Alwar'), ('Aizawl', 'Aizawl'), ('Bijāpur', 'Bijāpur'), ('Imphal', 'Imphal'), ('Tharati Etawah', 'Tharati Etawah'), ('Rāichūr', 'Rāichūr'), ('Pathānkot', 'Pathānkot'), ('Chīrāla', 'Chīrāla'), ('Sonīpat', 'Sonīpat'), ('Mirzāpur', 'Mirzāpur'), ('Hāpur', 'Hāpur'), ('Porbandar', 'Porbandar'), ('Bharatpur', 'Bharatpur'), ('Puducherry', 'Puducherry'), ('Karnāl', 'Karnāl'), ('Nāgercoil', 'Nāgercoil'), ('Thanjāvūr', 'Thanjāvūr'), ('Pāli', 'Pāli'), ('Agartala', 'Agartala'), ('Ongole', 'Ongole'), ('Puri', 'Puri'), ('Dindigul', 'Dindigul'), ('Haldia', 'Haldia'), ('Bulandshahr', 'Bulandshahr'), ('Purnea', 'Purnea'), ('Proddatūr', 'Proddatūr'), ('Gurgaon', 'Gurgaon'), ('Khānāpur', 'Khānāpur'), ('Machilīpatnam', 'Machilīpatnam'), ('Bhiwāni', 'Bhiwāni'), ('Nandyāl', 'Nandyāl'), ('Bhusāval', 'Bhusāval'), ('Bharauri', 'Bharauri'), ('Tonk', 'Tonk'), ('Sirsa', 'Sirsa'), ('Vizianagaram', 'Vizianagaram'), ('Vellore', 'Vellore'), ('Alappuzha', 'Alappuzha'), ('Shimla', 'Shimla'), ('Hindupur', 'Hindupur'), ('Bāramūla', 'Bāramūla'), ('Bakshpur', 'Bakshpur'), ('Dibrugarh', 'Dibrugarh'), ('Saidāpur', 'Saidāpur'), ('Navsāri', 'Navsāri'), ('Budaun', 'Budaun'), ('Cuddalore', 'Cuddalore'), ('Harīpur', 'Harīpur'), ('Krishnāpuram', 'Krishnāpuram'), ('Fyzābād', 'Fyzābād'), ('Silchar', 'Silchar'), ('Ambāla', 'Ambāla'), ('Krishnanagar', 'Krishnanagar'), ('Kolār', 'Kolār'), ('Kumbakonam', 'Kumbakonam'), ('Tiruvannāmalai', 'Tiruvannāmalai'), ('Pīlibhīt', 'Pīlibhīt'), ('Abohar', 'Abohar'), ('Port Blair', 'Port Blair'), ('Alīpur Duār', 'Alīpur Duār'), ('Hatīsa', 'Hatīsa'), ('Vālpārai', 'Vālpārai'), ('Aurangābād', 'Aurangābād'), ('Kohima', 'Kohima'), ('Gangtok', 'Gangtok'), ('Karūr', 'Karūr'), ('Jorhāt', 'Jorhāt'), ('Panaji', 'Panaji'), ('Saidpur', 'Saidpur'), ('Tezpur', 'Tezpur'), ('Itanagar', 'Itanagar'), ('Daman', 'Daman'), ('Silvassa', 'Silvassa'), ('Diu', 'Diu'), ('Dispur', 'Dispur'), ('Kavaratti', 'Kavaratti'), ('Calicut', 'Calicut'), ('Kagaznāgār', 'Kagaznāgār'), ('Jaipur', 'Jaipur'), ('Ghandinagar', 'Ghandinagar'), ('Panchkula', 'Panchkula')]
)
	submit = SubmitField("Submit")
	
	'''def validate_ssnid(self,ssn_id):
					customer = Customer.filter_by(ssn=ssn_id).first()
					if customer:
						raise ValidationError("SSN Id is already in use. Pick another one.")
					if len(ssn_id.data)>10:
						raise ValidationError("SSN Id should be not more than 9 digit numeric.")
					'''
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
