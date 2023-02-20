from app import db

from models.Account import Account

class Event(db.Model):

	__tablename__ = "events"

	id = db.Column(db.Integer, primary_key=True)

	points       = db.Column(db.Integer     , unique=False, nullable=False)
	title        = db.Column(db.String(256) , unique=False, nullable=False)
	room         = db.Column(db.String(256) , unique=False, nullable=False)
	author       = db.Column(db.String(256) , unique=False, nullable=False)
	start        = db.Column(db.Integer     , unique=False, nullable=False)
	duration     = db.Column(db.Integer     , unique=False, nullable=False)
	weblink      = db.Column(db.String(256) , unique=False, nullable=False)
	description  = db.Column(db.String(4096), unique=False, nullable=False)

	def __init__(self, points=0, title="", room="", author="", start=0, duration=0,
		weblink="", description=""):

		self.points       = points
		self.title        = title
		self.room         = room
		self.author       = author
		self.start        = start
		self.duration     = duration
		self.weblink      = weblink
		self.description  = description 

class Attendance(db.Model):
	"""
	Account <-> Event
	"""

	__tablename__ = "attendances"

	id = db.Column(db.Integer, primary_key=True)

	user  = db.Column(db.Integer, db.ForeignKey(Account.id), unique=False, nullable=False)
	event = db.Column(db.Integer, db.ForeignKey(Event.id)  , unique=False, nullable=False)

	def __init__(self, user=0, event=0):
		self.user  = user
		self.event = event

	def check_ne(user: int, event: int) -> bool:
		"""
		Return True if Attendance with user and event do not exist.
		"""

		try:
			assert Attendance.query.filter_by(user=user, event=event).first() == None
			return True
		except:
			return False

