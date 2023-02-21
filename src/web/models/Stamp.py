import time

from app import db

from models.Account import Account

class Stamp(db.Model):

	__tablename__ = "stamps"

	id = db.Column(db.Integer, primary_key=True)

	name      = db.Column(db.String(512), unique=False, nullable=False)
	slots     = db.Column(db.Integer    , unique=False, nullable=False)
	cooldown  = db.Column(db.Integer    , unique=False, nullable=False)

	def __init__(self, name="", slots=0, cooldown=0):
		self.name      = name
		self.slots     = slots
		self.cooldown  = cooldown

	def punches(self, user=0) -> int:
		return len(Punch.query.filter_by(stamp=self.id, user=user).all())

	def has_punches(self, user=0) -> bool:
		return self.punches(user) < self.slots

	def punch(self, user=0) -> bool:
		"""
		Return True if successfully punched, or False if on cooldown.
		"""

		punches = Punch.query.filter_by(stamp=self.id, user=user).all()
		latest = 0

		for punch in punches:
			if punch.time > latest:
				latest = punch.time

		if time.time() - latest > self.cooldown:
			punch = Punch(user=user, stamp=self.id)
			db.session.add(punch)
			db.session.commit()
			return True

		return False

class Punch(db.Model):
	"""
	Account <-> Stamp
	"""

	__tablename__ = "punches"

	id = db.Column(db.Integer, primary_key=True)

	user  = db.Column(db.Integer, db.ForeignKey(Account.id), unique=False, nullable=False)
	stamp = db.Column(db.Integer, db.ForeignKey(Stamp.id)  , unique=False, nullable=False)
	time  = db.Column(db.Integer, unique=False, nullable=False)

	def __init__(self, user=0, stamp=0):
		self.user  = user
		self.stamp = stamp
		self.time  = int(time.time())

