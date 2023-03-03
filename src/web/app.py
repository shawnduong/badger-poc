import sys

from flask import *
from flask_sqlalchemy import *

# Instantiate the application and define settings.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "YOUR_KEY_HERE"  # RNG str >16 B should suffice.

# Load the database.
db = SQLAlchemy(app)
from model import *
with app.app_context():
	db.create_all()

	from security import *
	from route import *
	from api import *
