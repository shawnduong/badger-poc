from app import *

@app.route("/api/stamp/create", methods=["POST"])
@login_required
def api_stamp_create():

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		stamp = Stamp(request.form["name"], int(request.form["slots"]),
			int(request.form["cooldown"])*60)
		db.session.add(stamp)
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "400 Bad Request"}, 400

@app.route("/api/stamp/list", methods=["GET"])
@login_required
def api_stamp_list():

	# Admins get a list of all stamps.
	if current_user.type == 1:
		try:
			stamps = Stamp.query.all()
			response = [{"id": s.id, "name": s.name, "slots": s.slots,
				"cooldown": int(s.cooldown)//60} for s in stamps]
			return {"Response": "200 OK", "Stamps": response}, 200
		except:
			return {"Response": "500 Internal Server Error"}, 500
	# Users get un/punched stamps.
	else:
		try:
			stamps = Stamp.query.all()
			stampings = Stampings.query.filter_by(user=current_user.id).all()
			stamped = [s.stamp for s in stampings]
			unstamped = [s.name for s in stamps if s.id not in stamped]
			stampedNames = [s.name for s in stamps if s.id in stamped]
			return {"Response": "200 OK", "Stamped": stampedNames, "Unstamped": unstamped}
		except:
			return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/stamp/delete/<id>", methods=["POST"])
@login_required
def api_stamp_delete(id):

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		stamp = Stamp.query.filter_by(id=int(id)).delete()
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/stamp/edit/<id>", methods=["POST"])
@login_required
def api_stamp_edit(id):

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		slots = int(request.form["slots"])
		stamp = Stamp.query.filter_by(id=int(id)).first()
		stamp.name = request.form["name"]
		stamp.slots = slots
		stamp.cooldown = int(request.form["cooldown"])*60
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/stamp/punch/list", methods=["GET"])
@login_required
def api_stamp_punch_list():

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:

		punches = []

		for p in Punch.query.all():
			u = Account.query.filter_by(id=p.user).first()
			s = Stamp.query.filter_by(id=p.stamp).first()
			punches.append({"id": p.id, "uid": f"{u.uid: 08X}", "name": u.name, "stamp": s.name})

		return {"Response": "200 OK", "Punches": punches}, 200

	except:
		return {"Response": "500 Internal Server Error"}, 500

