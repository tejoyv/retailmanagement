from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField,TextField,SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from application.models import User,Customer

class Registeration(FlaskForm):
    ssn_id = IntegerField("Customer SSN Id",validators=[DataRequired()])
    cust_name = StringField("Customer Name",validators=[DataRequired(),Length(max=30)])
    cust_age = IntegerField("Age",validators=[DataRequired()])
    address = TextField("Address",validators=[DataRequired(),Length(max=30)])
    state = SelectField("State",validators=[DataRequired()],choices=[("Gujarat","Gujarat"),("Maharashtra","Maharashtra")])
    city = SelectField("City",validators=[DataRequired()],choices=[("Ahmedabad","Ahemdabad"),("Pune","Pune")])
    submit = SubmitField("Submit")
    
    def validate_ssnid(self,ssn_id):
        customer = Customer.filter_by(ssn=ssn_id).first()
        if customer:
            raise ValidationError("SSN Id is already in use. Pick another one.")
        if len(ssn_id.data>10):
            raise ValidationError("SSN Id should be not more than 9 digit numeric")
        if len(cust_age.data>3):
            raise ValidationError("Age should be not more than 3 digit numeric")
