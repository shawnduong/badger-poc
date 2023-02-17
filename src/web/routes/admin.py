from app import *

from flask_login import current_user, login_required

@app.route("/admin/login", methods=["GET"])
def admin_login():

	if current_user.is_authenticated:
		return redirect(url_for("admin"))
	return render_template("admin/login.html")

@app.route("/admin", methods=["GET"])
@login_required
def admin():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/admin.html")

@app.route("/admin/password/change", methods=["GET"])
@login_required
def admin_password_change():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/password/change.html")

@app.route("/admin/announcements/manage", methods=["GET"])
@login_required
def admin_announcements_manage():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/announcements/manage.html")

@app.route("/admin/announcements/create", methods=["GET"])
@login_required
def admin_announcements_create():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/announcements/create.html")

@app.route("/admin/announcements/edit/<id>", methods=["GET"])
@login_required
def admin_announcements_edit(id):

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))

	a = Announcement.query.filter_by(id=id).first()
	return render_template("admin/announcements/edit.html", id=id,
		contents=a.contents, timestamp=a.timestamp)

@app.route("/admin/events/manage", methods=["GET"])
@login_required
def admin_events_manage():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/events/manage.html")

@app.route("/admin/events/create", methods=["GET"])
@login_required
def admin_events_create():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/events/create.html")

@app.route("/admin/events/edit/<id>", methods=["GET"])
@login_required
def admin_events_edit(id):

	# Admin only.
	if current_user.type != 1:
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

@app.route("/admin/codes", methods=["GET"])
@login_required
def admin_codes():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/codes.html")

@app.route("/admin/stamps", methods=["GET"])
@login_required
def admin_stamps():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/stamps.html")

@app.route("/admin/users", methods=["GET"])
@login_required
def admin_users():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/users.html")

