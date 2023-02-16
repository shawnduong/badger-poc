from datetime import datetime

from app import *

@app.route("/api/event/create", methods=["POST"])
@login_required
def api_event_create():

	# Admin only.
	if current_user.acctType != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:

		epoch = datetime(1970, 1, 1).replace(tzinfo=None)
		timezone = request.form["timezone"].replace(":", "")
		start = int((datetime.strptime(
			f"{request.form['start']} {timezone}",
			"%Y-%m-%dT%H:%M %z"
		)).timestamp())

		durstr = request.form["duration"]
		duration = 0

		if "h" in request.form["duration"]:
			duration += 3600 * int(durstr.split("h")[0])
			durstr = durstr.split("h")[1]
		if "m" in request.form["duration"]:
			duration += 60 * int(durstr.split("m")[0])

		event = Event(
			int(request.form["points"]),
			request.form["title"],
			request.form["location"],
			request.form["author"],
			start,
			duration,
			request.form["link"],
			request.form["description"]
		)
		db.session.add(event)
		db.session.commit()
		return {"Response": "200 OK"}, 200

	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/event/list", methods=["GET"])
@login_required
def api_event_list():

	try:
		events = []

		for e in Event.query.all():

			length = ""
			if (n:=(e.duration // 3600)) > 0:
				length += f"{n}h"
			if (n:=((e.duration % 3600) // 60)) > 0:
				length += f"{n}m"

			events.append({
				"id": e.id,
				"start": e.start,
				"length": length,
				"location": e.room,
				"title": e.title
			})

		return {"Response": "200 OK", "Events": events}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

@app.route("/api/event/delete/<id>", methods=["POST"])
@login_required
def api_event_delete(id):

	# Admin only.
	if current_user.acctType != 1:
		return {"Response": "401 Unauthorized"}, 401

	try:
		id = int(id)
		event = Event.query.filter_by(id=id).delete()
		db.session.commit()
		return {"Response": "200 OK"}, 200
	except:
		return {"Response": "500 Internal Server Error"}, 500

