from app import db

from models.Account import Account

class Stamp(db.Model):

	__tablename__ = "stamps"

	id = db.Column(db.Integer, primary_key=True)

	name  = db.Column(db.String(512), unique=False, nullable=False)
	slots = db.Column(db.Integer    , unique=False, nullable=False)

	def __init__(self, name="", slots=0):
		self.name  = name
		self.slots = slots

	def punches(self, user=0) -> int:
		return len(Punch.query.filter_by(stamp=self.id, user=user).all())

class Punch(db.Model):
	"""
	Account <-> Stamp
	"""

	__tablename__ = "punches"

	id = db.Column(db.Integer, primary_key=True)

	user  = db.Column(db.Integer, db.ForeignKey(Account.id), unique=False, nullable=False)
	stamp = db.Column(db.Integer, db.ForeignKey(Stamp.id)  , unique=False, nullable=False)

	def __init__(self, user=0, stamp=0):
		self.user  = user
		self.stamp = stamp

