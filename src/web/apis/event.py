import time

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

			if int(time.time()) > e.start + e.duration:
				status = 2  # Completed
			elif int(time.time()) > e.start and int(time.time()) < e.start + e.duration:
				status = 1  # Happening
			else:
				status = 0  # Not happened yet

			events.append({
				"id": e.id,
				"start": e.start,
				"length": length,
				"location": e.room,
				"title": e.title,
				"status": status
			})

		# Guarantee time order so that the earliest event is index 0.
		sortedEvents = [{"start":0}, {"start":2**32}]

		for e in events:
			for i in range(len(sortedEvents)-1):
				if e["start"] > sortedEvents[i]["start"] and e["start"] < sortedEvents[i+1]["start"]:
					sortedEvents.insert(i+1, e)
					break

		sortedEvents = sortedEvents[::-1]

		return {"Response": "200 OK", "Events": sortedEvents[1:-1]}, 200

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

@app.route("/api/event/edit/<id>", methods=["POST"])
@login_required
def api_event_edit(id):

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

		id = int(id)
		event = Event.query.filter_by(id=id).first()
		event.points = int(request.form["points"])
		event.title = request.form["title"]
		event.room = request.form["location"]
		event.author = request.form["author"]
		event.start = start
		event.duration = duration
		event.weblink = request.form["link"]
		event.description = request.form["description"]
		db.session.commit()
		return {"Response": "200 OK"}, 200

	except Exception as e:
		print(e)
		return {"Response": "500 Internal Server Error"}, 500

