from app import db

from models.Account import Account

class Prize(db.Model):

	__tablename__ = "prizes"

	id = db.Column(db.Integer, primary_key=True)

	prize     = db.Column(db.String(256), unique=False, nullable=False)
	value     = db.Column(db.Integer    , unique=False, nullable=False)
	quantity  = db.Column(db.Integer    , unique=False, nullable=False)

	def __init__(self, prize="", value=0, quantity=""):
		self.prize     = prize
		self.value     = prize
		self.quantity  = prize

class Redemption(db.Model):
	"""
	Account <-> Prize
	"""

	__tablename__ = "redemptions"

	id = db.Column(db.Integer, primary_key=True)

	user  = db.Column(db.Integer, db.ForeignKey(Account.id), unique=False, nullable=False)
	prize = db.Column(db.Integer, db.ForeignKey(Prize.id)  , unique=False, nullable=False)

	def __init__(self, user=0, prize=0):
		self.user  = user
		self.prize = prize

