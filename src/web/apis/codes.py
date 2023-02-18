from app import *

@app.route("/api/code/create", methods=["POST"])
@login_required
def api_code_create():

	# Admin only.
	if current_user.type != 1:
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
	if current_user.type != 1:
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
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		code = Code.query.filter_by(id=int(id)).delete()
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/code/submit/<code>", methods=["POST"])
@login_required
def api_code_submit(code):

	try:
		user = current_user.id
		c = Code.query.filter_by(code=str(code)).first().id
		assert len(CodeRedemption.query.filter_by(user=user, code=c).all()) == 0
		redemption = CodeRedemption(user, c)
		db.session.add(redemption)
		db.session.commit()
		current_user.update_points()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "400 Bad Request"}, 400

@app.route("/api/code/edit/<id>", methods=["POST"])
@login_required
def api_code_edit(id):

	# Admin only.
	if current_user.type != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		code = Code.query.filter_by(id=int(id)).first()
		code.code = request.form["code"]
		code.value = request.form["value"]
		code.note = request.form["note"]
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

