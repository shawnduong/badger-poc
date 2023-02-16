from app import *

@app.route("/api/code/create", methods=["POST"])
@login_required
def api_code_create():

	# Admin only.
	if current_user.acctType != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		code = request.form["code"]
		value = int(request.form["value"])
		note = request.form["note"]
		c = Code(code, value, note)
		db.session.add(c)
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "400 Bad Request"}, 400

@app.route("/api/code/list", methods=["GET"])
@login_required
def api_code_list():

	# Admin only.
	if current_user.acctType != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		codes = Code.query.all()
		response = [{"id": c.id, "code": c.code, "value": c.value, "note": c.note}
			for c in codes]
		return {"Response": "200 OK", "Codes": response}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/code/delete/<id>", methods=["POST"])
@login_required
def api_code_delete(id):

	# Admin only.
	if current_user.acctType != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		id = int(id)
		code = Code.query.filter_by(id=id).delete()
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

