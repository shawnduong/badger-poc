from app import db

class Announcement(db.Model):

	__tablename__ = "announcements"

	id = db.Column(db.Integer, primary_key=True)

	timestamp = db.Column(db.Integer     , unique=False, nullable=False)
	contents  = db.Column(db.String(4096), unique=False, nullable=False)

	def __init__(self, timestamp=0, contents=""):
		self.timestamp = timestamp
		self.contents  = contents

