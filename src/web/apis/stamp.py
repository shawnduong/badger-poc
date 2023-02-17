from app import *

@app.route("/api/stamp/create", methods=["POST"])
@login_required
def api_stamp_create():

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		name = request.form["name"]
		stamp = Stamp(name)
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
			response = [{"id": s.id, "name": s.name} for s in stamps]
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
		id = int(id)
		stamp = Stamp.query.filter_by(id=id).delete()
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

