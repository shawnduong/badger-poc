from app import *

@app.route("/api/reward/create", methods=["POST"])
@login_required
def api_reward_create():

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		value = int(request.form["value"])
		stock = int(request.form["stock"])
		r = Reward(request.form["reward"], value, stock)
		db.session.add(r)
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "400 Bad Request"}, 400

@app.route("/api/reward/list", methods=["GET"])
@login_required
def api_reward_list():

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		rewards = Reward.query.all()
		response = [{"id": r.id, "reward": r.reward, "value": r.value,
			"stock": r.stock, "claims": r.claimed()} for r in rewards]
		return {"Response": "200 OK", "Rewards": response}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/reward/delete/<id>", methods=["POST"])
@login_required
def api_reward_delete(id):

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		reward = Reward.query.filter_by(id=int(id)).delete()
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/reward/edit/<id>", methods=["POST"])
@login_required
def api_reward_edit(id):

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		value = int(request.form["value"])
		stock = int(request.form["stock"])
		reward = Reward.query.filter_by(id=int(id)).first()
		reward.reward = request.form["reward"]
		reward.value = value
		reward.stock = stock
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/reward/redeem/<id>", methods=["POST"])
@login_required
def api_reward_redeem(id):

	try:
		reward = Reward.query.filter_by(id=int(id)).first()
		assert reward.remaining() > 0
		assert reward.can_afford(current_user) > 0
		assert reward.limit_one(current_user.id) > 0
		redemption = Redemption(current_user.id, reward.id)
		db.session.add(redemption)
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except Exception as e:
		return {"Response": "500 Internal Server Error"}, 500

