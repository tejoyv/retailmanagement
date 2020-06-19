from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Email


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
