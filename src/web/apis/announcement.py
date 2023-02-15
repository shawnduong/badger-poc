from app import *

@app.route("/api/announcement/create", methods=["POST"])
@login_required
def api_announcement_create():

	# Admin only.
	if current_user.acctType != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		timestamp = int(request.form["timestamp"])
		assert len(request.form["content"]) <= 2048
		announcement = Announcement(timestamp, request.form["content"])
		db.session.add(announcement)
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/announcement/list", methods=["GET"])
@login_required
def api_announcement_list():

	try:
		ann = Announcement.query.all()
		r = [{"id": a.id, "timestamp": a.timestamp, "contents": a.contents} for a in ann]
		return {"Response": "200 OK", "Announcements": r}, 200
	except Exception as e:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/announcement/delete/<id>", methods=["POST"])
@login_required
def api_announcement_delete(id):

	# Admin only.
	if current_user.acctType != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		id = int(id)
		announcement = Announcement.query.filter_by(id=id).delete()
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

