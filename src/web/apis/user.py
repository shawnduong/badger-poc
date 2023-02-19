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
			"email": u.email, "points": u.points} for u in users]
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
		return {
			"Response": "200 OK",
			"User": {
				"uid": f"{current_user.uid: 08x}",
				"name": current_user.name,
				"email": current_user.email,
				"points": current_user.points,
			}
		}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

