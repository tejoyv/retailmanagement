from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail,Message

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

from application.customers.routes import customers
from application.main.routes import main
from application.accounts.routes import accounts

app.register_blueprint(customers)
app.register_blueprint(main)
app.register_blueprint(accounts)