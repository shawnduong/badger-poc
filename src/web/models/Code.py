from app import db

from models.Account import Account

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

	def check_ne(user: int, code: int) -> bool:
		"""
		Return True if Submit with user and code do not exist.
		"""

		try:
			assert len(Submit.query.filter_by(user=user, code=code).all()) == 0
			return True
		except:
			return False

