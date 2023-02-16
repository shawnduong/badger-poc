from app import *

from flask_login import current_user, login_required

@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET"])
def index():

	if current_user.is_authenticated:
		return redirect(url_for("application"))
	return render_template("index.html")

@app.route("/app", methods=["GET"])
@login_required
def application():

	# Admin redirect to admin panel.
	if current_user.acctType == 1:
		return redirect(url_for("admin"))
	return render_template("app.html")

@app.route("/event/<id>", methods=["GET"])
@login_required
def event(id):

	if current_user.acctType == 1:
		backlink = "/admin/events/manage"
	else:
		backlink = "/app"

	try:

		id = int(id)
		e = Event.query.filter_by(id=id).first()

		length = ""
		if (n:=(e.duration // 3600)) > 0:
			length += f"{n}h"
		if (n:=((e.duration % 3600) // 60)) > 0:
			length += f"{n}m"

		weblink = ""
		if e.weblink != None:
			weblink = e.weblink

		return render_template("event.html",
			backlink=backlink,
			title=e.title,
			author=e.author,
			location=e.room,
			start=e.start,
			duration=length,
			points=e.points,
			weblink=weblink,
			description=e.description
		)

	except:
		pass  # Automatic 404

@app.route("/admin/login", methods=["GET"])
def admin_login():

	if current_user.is_authenticated:
		return redirect(url_for("admin"))
	return render_template("admin/login.html")

@app.route("/admin", methods=["GET"])
@login_required
def admin():

	# Admin only.
	if current_user.acctType != 1:
		return redirect(url_for("index"))
	return render_template("admin/admin.html")

@app.route("/admin/change-password", methods=["GET"])
@login_required
def admin_change_password():

	# Admin only.
	if current_user.acctType != 1:
		return redirect(url_for("index"))
	return render_template("admin/change-password.html")

@app.route("/admin/announcements/manage", methods=["GET"])
@login_required
def admin_announcements_manage():

	# Admin only.
	if current_user.acctType != 1:
		return redirect(url_for("index"))
	return render_template("admin/announcements/manage.html")

@app.route("/admin/announcements/create", methods=["GET"])
@login_required
def admin_announcements_create():

	# Admin only.
	if current_user.acctType != 1:
		return redirect(url_for("index"))
	return render_template("admin/announcements/create.html")

@app.route("/admin/announcements/edit/<id>", methods=["GET"])
@login_required
def admin_announcements_edit(id):

	# Admin only.
	if current_user.acctType != 1:
		return redirect(url_for("index"))

	a = Announcement.query.filter_by(id=id).first()
	return render_template("admin/announcements/edit.html", id=id,
		contents=a.contents, timestamp=a.timestamp)

@app.route("/admin/events/manage", methods=["GET"])
@login_required
def admin_events_manage():

	# Admin only.
	if current_user.acctType != 1:
		return redirect(url_for("index"))
	return render_template("admin/events/manage.html")

@app.route("/admin/events/create", methods=["GET"])
@login_required
def admin_events_create():

	# Admin only.
	if current_user.acctType != 1:
		return redirect(url_for("index"))
	return render_template("admin/events/create.html")

@app.route("/admin/events/edit/<id>", methods=["GET"])
@login_required
def admin_events_edit(id):

	# Admin only.
	if current_user.acctType != 1:
		return redirect(url_for("index"))

	e = Event.query.filter_by(id=id).first()

	hours = 0
	minutes = 0

	if (n:=(e.duration // 3600)) > 0:
		hours = n
	if (n:=((e.duration % 3600) // 60)) > 0:
		minutes = n

	return render_template("admin/events/edit.html",
		id=id,
		title=e.title,
		author=e.author,
		room=e.room,
		start=e.start,
		hours=hours,
		minutes=minutes,
		points=e.points,
		weblink=e.weblink,
		description=e.description
	)

@app.route("/admin/users", methods=["GET"])
@login_required
def admin_users():

	# Admin only.
	if current_user.acctType != 1:
		return redirect(url_for("index"))
	return render_template("admin/users.html")

