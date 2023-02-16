from __future__ import annotations

import bcrypt

from app import db

from flask_login import UserMixin
from typing import Union

class Account(UserMixin, db.Model):
	"""
	Users (0) deliberately have lax security to ensure minimal setup and ease
	of use for non-tech participants. Admins (1) have strict security and are
	purely web; they do not have cards, and it is impossible to log in as admin
	using a card ID. Locators (2) are special cards that identify the scanned
	unit on the admin web interface.
	"""

	__tablename__ = "accounts"

	id = db.Column(db.Integer, primary_key=True)

	# 0 => user, 1 => admin, 2 => locator
	acctType = db.Column(db.Integer, unique=False, nullable=False)
	password = db.Column(db.String(256), unique=False, nullable=True)

	# cardID is the MFC UID (4 or 7 bytes).
	cardID  = db.Column(db.Integer    , unique=True , nullable=True)
	name    = db.Column(db.String(256), unique=False, nullable=True)
	email   = db.Column(db.String(256), unique=False, nullable=True)
	points  = db.Column(db.Integer    , unique=False, nullable=True)

	def __init__(self, acctType=0, password=None, cardID=0, name=None,
		email=None, points=0):

		self.acctType  = acctType
		self.password  = password
		self.cardID    = cardID
		self.name      = name
		self.email     = email
		self.points    = points

		if acctType == 1:
			self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(4))

	def get_user(cardID: str) -> Union[Account, bool]:
		"""
		Check if a cardID string is valid and return the Account if so. Else,
		return False. This is similar to the login function, except users in
		Badger log in using a card ID instead of a username/password.
		"""

		# Convert the cardID string from hex to an integer.
		try:
			intCardID = int(cardID, 16)
		except:
			return False

		if (user:=Account.query.filter_by(cardID=intCardID).first()) != None:
			return user

		return False

	def login(username: str, password: str) -> Union[Account, bool]:
		"""
		This is reserved for the admin. Check if the username/password are
		valid and return the Account if so. Else, return False.
		"""

		try:
			if ((user:=Account.query.filter_by(name=username).first()) != None
				and bcrypt.checkpw(password.encode(), user.password)):
				return user
		except:
			pass

		return False

	def update_points(self):
		"""
		Update the user's points as the sum of their attendances.
		"""

		self.points = 0
		attendances = Attendance.query.filter_by(user=self.id).all()

		for attendance in attendances:
			event = Event.query.filter_by(id=attendance.event).first()
			self.points += event.points

		db.session.commit()

class Event(db.Model):
	"""
	Events. Note that the times are epoch time. If a weblink is present, then
	the user may click the link to learn more about the event externally.
	"""

	__tablename__ = "events"

	id = db.Column(db.Integer, primary_key=True)

	points      = db.Column(db.Integer    , unique=False, nullable=False)
	title       = db.Column(db.String(256), unique=False, nullable=False)
	room        = db.Column(db.String(256) , unique=False, nullable=False)
	author      = db.Column(db.String(256) , unique=False, nullable=False)
	start       = db.Column(db.Integer     , unique=False, nullable=False)
	duration    = db.Column(db.Integer     , unique=False, nullable=False)
	weblink     = db.Column(db.String(256) , unique=False, nullable=True )
	description = db.Column(db.String(4096), unique=False, nullable=False)

	def __init__(self, points=0, title="", room="", author="",
		start=0, duration=0, weblink=None, description=""):
		"""
		Constructor method for Event type objects.
		"""

		self.points      = points
		self.title       = title
		self.room        = room
		self.author      = author
		self.start       = start
		self.duration    = duration
		self.weblink     = weblink
		self.description = description 

class Attendance(db.Model):
	"""
	Relate a Account to an Event.
	"""

	__tablename__ = "attendances"

	id = db.Column(db.Integer, primary_key=True)
	user  = db.Column(db.Integer, db.ForeignKey(Account.id), unique=False, nullable=False)
	event = db.Column(db.Integer, db.ForeignKey(Event.id), unique=False, nullable=False)

	def __init__(self, user=0, event=0):
		self.user  = user
		self.event = event

class Announcement(db.Model):
	"""
	Simple timestamp and HTML contents.
	"""

	__tablename__ = "announcements"

	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.Integer     , unique=False, nullable=False)
	contents  = db.Column(db.String(4096), unique=False, nullable=False)

	def __init__(self, timestamp=0, contents=""):
		self.timestamp = timestamp
		self.contents  = contents

class Code(db.Model):
	"""
	Points addition code.
	"""

	__tablename__ = "codes"

	id = db.Column(db.Integer, primary_key=True)
	code  = db.Column(db.String(64) , unique=True , nullable=False)
	value = db.Column(db.Integer    , unique=False, nullable=False)
	note  = db.Column(db.String(128), unique=True , nullable=False)

	def __init__(self, code="", value=0, note=""):
		self.code  = code
		self.value = value
		self.note  = note

