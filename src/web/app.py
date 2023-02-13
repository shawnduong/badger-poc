import sys

from flask import *
from flask_sqlalchemy import *

from keys import FLASK_SECRET_KEY

# Instantiate the application and define settings.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = FLASK_SECRET_KEY

# Load the database.
db = SQLAlchemy(app)
from models import *
with app.app_context():
	db.create_all()

# If there is no admin account, make a default one.
if Account.query.filter_by(name="admin", acctType=1).first() == None:
	admin = Account(1, "password", None, "admin", None, None)
	db.session.add(admin)
	db.session.commit()

# Authentication.
from authentication import *

# Website routes.
from routes import *

# API endpoints.
from api import *
