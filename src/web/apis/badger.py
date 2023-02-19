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
		approved = [{"id": b.id, "identity": f"{b.identity:08X}", "mode": b.mode(),
			"event": b.event()} for b in badgers if b.approved == 2]
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

#	print(request.json["id"])

	# Testing value.
	return {"Response": "200 OK", "rcode": 0}, 200
