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
		Update the user's points as Attendances + Submits - Redemptions.
		"""

		self.points = 0

		submits = Submit.query.filter_by(user=self.id).all()
		attendances = Attendance.query.filter_by(user=self.id).all()
		redemptions = Redemption.query.filter_by(user=self.id).all()

		for submit in submits:
			try:
				code = Code.query.filter_by(id=submit.code).first()
				self.points += code.value
			except:
				continue

		for attendance in attendances:
			try:
				event = Event.query.filter_by(id=attendance.event).first()
				self.points += event.points
			except:
				continue

		for redemption in redemptions:
			try:
				reward = Reward.query.filter_by(id=redemption.reward).first()
				self.points -= reward.value
			except:
				continue

		db.session.commit()
		return self.points

from models.Code import Code, Submit
from models.Event import Event, Attendance
from models.Reward import Reward, Redemption
