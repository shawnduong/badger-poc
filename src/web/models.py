from __future__ import annotations

import bcrypt

from app import db

from flask_login import UserMixin
from typing import Union

class Account(UserMixin, db.Model):

	__tablename__ = "accounts"

	id = db.Column(db.Integer, primary_key=True)

	# type: 0 => user, 1 => admin, 2 => locator
	type      = db.Column(db.Integer    , unique=False, nullable=False)
	password  = db.Column(db.String(256), unique=False, nullable=True )
	uid       = db.Column(db.Integer    , unique=True , nullable=True )
	name      = db.Column(db.String(256), unique=False, nullable=True )
	email     = db.Column(db.String(256), unique=False, nullable=True )
	points    = db.Column(db.Integer    , unique=False, nullable=True )

	def __init__(self, type=0, password=None, uid=0, name=None, email=None, points=0):

		self.type      = type
		self.password  = password
		self.uid       = uid
		self.name      = name
		self.email     = email
		self.points    = points

		if type == 1:
			self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(4))

	def get_user(uid: str) -> Union[Account, bool]:
		"""
		Get a user using an 8 or 14 hex char string.
		"""

		try:
			assert (user:=Account.query.filter_by(uid=int(uid, 16)).first()) != None
			return user
		except:
			return False

	def login(username: str, password: str) -> Union[Account, bool]:
		"""
		Log into the admin account.
		"""

		try:
			assert (user:=Account.query.filter_by(name=username).first()) != None
			assert bcrypt.checkpw(password.encode(), user.password)
			return user
		except:
			return False

	def update_points(self):
		"""
		Update the user's points as attendances+submits-redemptions.
		"""

		self.points = 0

		submits = Submits.query.filter_by(user=self.id).all()
		attendances = Attendance.query.filter_by(user=self.id).all()
		redemptions = Redemption.query.filter_by(user=self.id).all()

		for submit in submits:
			code = Code.query.filter_by(id=submit.code).first()
			self.points += code.points

		for attendance in attendances:
			event = Event.query.filter_by(id=attendance.event).first()
			self.points += event.points

		for redemption in redemptions:
			reward = Reward.query.filter_by(id=redemption.reward).first()
			self.points -= reward.value

		db.session.commit()

class Code(db.Model):

	__tablename__ = "codes"

	id = db.Column(db.Integer, primary_key=True)

	code  = db.Column(db.String(128), unique=True , nullable=False)
	value = db.Column(db.Integer    , unique=False, nullable=False)
	note  = db.Column(db.String(128), unique=True , nullable=False)

	def __init__(self, code="", value=0, note=""):
		self.code  = code
		self.value = value
		self.note  = note

class Submit(db.Model):
	"""
	Account <-> Code
	"""

	__tablename__ = "submits"

	id = db.Column(db.Integer, primary_key=True)

	user = db.Column(db.Integer, db.ForeignKey(Account.id), unique=False, nullable=False)
	code = db.Column(db.Integer, db.ForeignKey(Code.id)   , unique=False, nullable=False)

	def __init__(self, user=0, code=0):
		self.user = user
		self.code = code

	def check_ne(self, user, code):
		"""
		Return True if Submit with user and code do not exist.
		"""

		try:
			assert Code.query.filter_by(user=user, code=code).first() == None
			return True
		except:
			return False

class Event(db.Model):

	__tablename__ = "events"

	id = db.Column(db.Integer, primary_key=True)

	points       = db.Column(db.Integer     , unique=False, nullable=False)
	title        = db.Column(db.String(256) , unique=False, nullable=False)
	room         = db.Column(db.String(256) , unique=False, nullable=False)
	author       = db.Column(db.String(256) , unique=False, nullable=False)
	start        = db.Column(db.Integer     , unique=False, nullable=False)
	duration     = db.Column(db.Integer     , unique=False, nullable=False)
	weblink      = db.Column(db.String(256) , unique=False, nullable=True )
	description  = db.Column(db.String(4096), unique=False, nullable=False)

	def __init__(self, points=0, title="", room="", author="", start=0, duration=0,
		weblink=None, description=""):

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

	def check_ne(self, user, event):
		"""
		Return True if Attendance with user and event do not exist.
		"""

		try:
			assert Attendance.query.filter_by(user=user, event=event).first() == None
			return True
		except:
			return False

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

class Stamp(db.Model):

	__tablename__ = "stamps"

	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String(512), unique=False, nullable=False)

	def __init__(self, name=""):
		self.name = name

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

	def check_ne(self, user, stamp):
		"""
		Return True if Punch with user and stamp do not exist.
		"""

		try:
			assert Punch.query.filter_by(user=user, stamp=stamp).first() == None
			return True
		except:
			return False

class Announcement(db.Model):

	__tablename__ = "announcements"

	id = db.Column(db.Integer, primary_key=True)

	timestamp = db.Column(db.Integer     , unique=False, nullable=False)
	contents  = db.Column(db.String(4096), unique=False, nullable=False)

	def __init__(self, timestamp=0, contents=""):
		self.timestamp = timestamp
		self.contents  = contents

