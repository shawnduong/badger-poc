import time

from app import db

class Badger(db.Model):

	__tablename__ = "badgers"

	id = db.Column(db.Integer, primary_key=True)

	# approved: 0 => not approved, 1 => pending, 2 => approved
	# status: 0 => no status, 1 => attendance, 2 => rewards, 3 => stamps,
	#         4 => provisionment
	# tending is the ID of the event or stamp it's associated with.
	identity  = db.Column(db.Integer, unique=True , nullable=False)
	approved  = db.Column(db.Integer, unique=False, nullable=False)
	status    = db.Column(db.Integer, unique=False, nullable=False)
	tending   = db.Column(db.Integer, unique=False, nullable=False)
	lastSeen  = db.Column(db.Integer, unique=False, nullable=False)
	located   = db.Column(db.Integer, unique=False, nullable=False)

	def __init__(self, identity=0, approved=0, status=0, tending=0, lastSeen=0, located=0):
		self.identity  = identity
		self.approved  = approved
		self.status    = status
		self.tending   = tending
		self.lastSeen  = lastSeen
		self.located   = located

	def alive(self):
		self.lastSeen = int(time.time())
		db.session.commit()

	def auth_request(identity=0):

		badger = Badger.query.filter_by(identity=identity).first()

		if badger == None:
			badger = Badger(identity, 1, 0, 0, int(time.time()))
			db.session.add(badger)
			db.session.commit()
			return False

		badger.alive()
		return badger.approved == 2

	def auth_approve(self):
		self.approved = 2
		db.session.commit()

	def mode(self) -> str:
		"""
		Return the string representation of the current mode.
		"""

		if self.status == 0:
			return "Idle"
		elif self.status == 1:
			return "Attendance"
		elif self.status == 2:
			return "Rewards"
		elif self.status == 3:
			return "Stamps"
		elif self.status == 4:
			return "Provisionment"

		return "Unexpected error occurred."

	def event(self) -> str:
		"""
		Return the string representation of the current event.
		"""

		if self.status == 0:
			return "N/A"
		elif self.status == 1:
			e = Event.query.filter_by(id=self.tending).first()
			return e.title
		elif self.status == 2:
			return "N/A"
		elif self.status == 3:
			s = Stamp.query.filter_by(id=self.tending).first()
			return s.name
		elif self.status == 4:
			return "N/A"

		return "Unexpected error occurred."

	def locate(self):
		"""
		Upon scanning a locator, set this Badger's located timestamp.
		"""

		self.located = int(time.time())
		db.session.commit()

	def is_located(self) -> bool:
		"""
		Return True if located in the past 5 seconds.
		"""

		return time.time()-5 < self.located

from models.Event import Event
from models.Stamp import Stamp
