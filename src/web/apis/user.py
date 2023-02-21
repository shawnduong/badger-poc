from app import *

@app.route("/api/user/create", methods=["POST"])
@login_required
def api_user_create():

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		uid = int(request.form["uid"], 16)
		user = Account(uid=uid)
		db.session.add(user)
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "400 Bad Request"}, 400

@app.route("/api/user/list", methods=["GET"])
@login_required
def api_user_list():

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		users = Account.query.filter_by(type=0).all()
		response = [{"id": u.id, "uid": hex(u.uid)[2:].zfill(8), "name": u.name,
			"email": u.email, "points": u.update_points()} for u in users]
		return {"Response": "200 OK", "Users": response}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/user/delete/<id>", methods=["POST"])
@login_required
def api_user_delete(id):

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		account = Account.query.filter_by(id=int(id)).delete()
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/user/edit/name", methods=["POST"])
@login_required
def api_user_edit_name():

	try:
		current_user.name = request.form["name"]
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/user/edit/email", methods=["POST"])
@login_required
def api_user_edit_email():

	try:
		current_user.email = request.form["email"]
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/user/info", methods=["GET"])
@login_required
def api_user_info():

	try:

		current_user.update_points()
		stamps = [{"name": s.name, "slots": s.slots, "punches": s.punches(current_user.id)}
			for s in Stamp.query.all()]
		rewards = [{"id": r.id, "reward": r.reward, "value": r.value, "stock": r.remaining(),
			"status": r.status(current_user.id)} for r in Reward.query.all()]

		breakdown = []

		for a in Attendance.query.filter_by(user=current_user.id).all():
			e = Event.query.filter_by(id=a.event).first()
			breakdown.append(f"+{e.points} Attended \"{e.title}\"")

		for c in Submit.query.filter_by(user=current_user.id).all():
			c = Code.query.filter_by(id=c.code).first()
			breakdown.append(f"+{c.value} Submitted code \"{c.note}\"")

		for r in Redemption.query.filter_by(user=current_user.id).all():
			rw = Reward.query.filter_by(id=r.reward).first()
			breakdown.append(f"-{rw.value} Redeemed reward \"{rw.reward}\"")

		return {
			"Response": "200 OK",
			"User": {
				"uid": f"{current_user.uid: 08X}",
				"name": current_user.name,
				"email": current_user.email,
				"points": current_user.points,
				"stamps": stamps,
				"rewards": rewards,
				"breakdown": breakdown,
			}
		}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/user/locator/create", methods=["POST"])
@login_required
def api_user_locator_create():

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		uid = int(request.form["uid"], 16)
		user = Account(uid=uid, type=2)
		db.session.add(user)
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "400 Bad Request"}, 400

@app.route("/api/user/locator/list", methods=["GET"])
@login_required
def api_user_locator_list():

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		users = Account.query.filter_by(type=2).all()
		response = [{"id": u.id, "uid": hex(u.uid)[2:].zfill(8)} for u in users]
		return {"Response": "200 OK", "Users": response}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

