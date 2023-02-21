from app import db

from models.Account import Account

class Reward(db.Model):

	__tablename__ = "rewards"

	id = db.Column(db.Integer, primary_key=True)

	reward = db.Column(db.String(256), unique=False, nullable=False)
	value  = db.Column(db.Integer    , unique=False, nullable=False)
	stock  = db.Column(db.Integer    , unique=False, nullable=False)

	def __init__(self, reward="", value=0, stock=0):
		self.reward = reward
		self.value = value
		self.stock = stock

	def can_afford(self, user) -> bool:
		user.update_points()
		return user.points >= self.value

	def limit_one(self, user=0) -> bool:
		return len(Redemption.query.filter_by(user=user, reward=self.id).all()) == 0

	def status(self, user=0) -> int:
		"""
		Returns 0 if not redeemed, 1 if redeemed but not claimed, and 2 if claimed.
		"""

		if (r:=Redemption.query.filter_by(user=user, reward=self.id).first()) == None:
			return 0

		if r.claimed == False:
			return 1

		return 2

	def claimed(self) -> int:

		return len(Redemption.query.filter_by(reward=self.id).all())

	def remaining(self) -> int:

		return self.stock - self.claimed()

class Redemption(db.Model):
	"""
	Account <-> Reward
	"""

	__tablename__ = "redemptions"

	id = db.Column(db.Integer, primary_key=True)

	user      = db.Column(db.Integer, db.ForeignKey(Account.id), unique=False, nullable=False)
	reward    = db.Column(db.Integer, db.ForeignKey(Reward.id) , unique=False, nullable=False)
	claiming  = db.Column(db.Boolean, unique=False, nullable=False)
	claimed   = db.Column(db.Boolean, unique=False, nullable=False)

	def __init__(self, user=0, reward=0, claiming=False, claimed=False):
		self.user      = user
		self.reward    = reward
		self.claiming  = claiming
		self.claimed   = claimed

	def do_claiming(self):
		self.claiming = True
		db.session.commit()

	def claim(self):
		self.claiming  = False
		self.claimed   = True
		db.session.commit()

