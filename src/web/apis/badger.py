from app import *

@app.route("/api/badger/identify", methods=["POST"])
def api_badger_identify():

	try:
		assert Badger.auth_request(int(request.args.get("identity")))
	except:
		return {"Response": "401 Unauthorized"}, 401

	return {"Response": "200 OK"}, 200

@app.route("/api/badger/list", methods=["GET"])
@login_required
def api_badger_list():

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		badgers = Badger.query.all()
		pending = [{"id": b.id, "identity": f"{b.identity:08X}"} for b in badgers if b.approved != 2]
		approved = [{"id": b.id, "identity": f"{b.identity:08X}", "located": b.is_located(), "mode": b.mode(),
			"event": b.event(), "lastSeen": b.lastSeen} for b in badgers if b.approved == 2]
		return {"Response": "200 OK", "Pending": pending, "Approved": approved}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/badger/approve/<id>", methods=["POST"])
@login_required
def api_badger_approve(id):

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		b = Badger.query.filter_by(id=int(id)).first()
		b.auth_approve()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/badger/delete/<id>", methods=["POST"])
@login_required
def api_badger_delete(id):

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		Badger.query.filter_by(id=int(id)).delete()
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/badger/scan", methods=["POST"])
def api_badger_scan():

	try:
		assert Badger.auth_request(int(request.args.get("identity")))
	except:
		return {"Response": "401 Unauthorized", "rcode": 3}, 401

	try:

		# Find the badger.
		b = Badger.query.filter_by(identity=int(request.args.get("identity"))).first()

		# If a locator card was scanned, highlight this Badger.
		try:
			user = Account.query.filter_by(uid=int(request.json["id"])).first()
			assert user.type == 2
			b.locate()
			return {"Response": "200 OK", "rcode": 1}, 200
		except:
			pass

		# Idle mode.
		if b.status == 0:

			# RGB red and blue.
			return {"Response": "200 OK", "rcode": -1}, 200

		# Attendance mode.
		elif b.status == 1:

			# Find the user.
			user = Account.query.filter_by(uid=int(request.json["id"])).first()
			assert user != None

			# Find the event.
			event = Event.query.filter_by(id=b.tending).first()
			assert event != None

			# Make sure an attendance doesn't exist.
			if Attendance.check_ne(user.id, event.id):

				attendance = Attendance(user.id, event.id)
				db.session.add(attendance)
				db.session.commit()

				# Green.
				return {"Response": "200 OK", "rcode": 1}, 200

			# Blue.
			return {"Response": "200 OK", "rcode": 2}, 200

		# Rewards mode.
		elif b.status == 2:

			# Find the user.
			user = Account.query.filter_by(uid=int(request.json["id"])).first()
			assert user != None

			# Find all of their redemptions that are unclaimed.
			claimings = Redemption.query.filter_by(user=user.id, claiming=False, claimed=False).all()

			# Set all of them to claiming.
			for c in claimings:
				c.do_claiming()

			# Green.
			return {"Response": "200 OK", "rcode": 1}, 200

		# Stamp mode.
		elif b.status == 3:

			# Find the user.
			user = Account.query.filter_by(uid=int(request.json["id"])).first()
			assert user != None

			# Find the stamp.
			stamp = Stamp.query.filter_by(id=b.tending).first()
			assert stamp != None

			assert stamp.has_punches(user.id)

			# Try to punch the user. LED green if not on cooldown.
			if stamp.punch(user.id):
				return {"Response": "200 OK", "rcode": 1}, 200

			# On cooldown. Blue.
			return {"Response": "200 OK", "rcode": 2}, 200

		# Provisionment mode.
		elif b.status == 4:

			# Make sure the user doesn't exist.
			if Account.query.filter_by(uid=int(request.json["id"])).first() != None:
				return {"Response": "200 OK", "rcode": 2}, 200

			# Make the user.
			account = Account(uid=int(request.json["id"]))
			db.session.add(account)
			db.session.commit()

			# Green.
			return {"Response": "200 OK", "rcode": 1}, 200

	except:

		# RGB red.
		return {"Response": "200 OK", "rcode": 0}, 200

@app.route("/api/badger/configurations", methods=["GET"])
@login_required
def api_badger_configurations():

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		events = [{"id": e.id, "title": e.title} for e in Event.query.all()]
		stamps = [{"id": s.id, "name" : s.name } for s in Stamp.query.all()]
		return {"Response": "200 OK", "Events": events, "Stamps": stamps}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/badger/configure/<id>", methods=["POST"])
@login_required
def api_badger_configure(id):

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:

		data = request.form["option"].split(";")
		status  = int(data[0])
		tending = int(data[1])

		badger = Badger.query.filter_by(id=int(id)).first()
		badger.status  = status
		badger.tending = tending 

		db.session.commit()
		return {"Response": "200 OK"}, 200

	except:
		return {"Response": "400 Bad Request"}, 400

