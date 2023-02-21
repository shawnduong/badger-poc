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

	a = Announcement.query.filter_by(id=int(id)).first()
	return render_template("admin/announcements/edit.html", id=a.id,
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

	e = Event.query.filter_by(id=int(id)).first()

	hours = 0
	minutes = 0

	if (n:=(e.duration // 3600)) > 0:
		hours = n
	if (n:=((e.duration % 3600) // 60)) > 0:
		minutes = n

	return render_template("admin/events/edit.html",
		id=e.id,
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

@app.route("/admin/events/attendances", methods=["GET"])
@login_required
def admin_events_attendances():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/events/attendances.html")

@app.route("/admin/codes/manage", methods=["GET"])
@login_required
def admin_codes_manage():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/codes/manage.html")

@app.route("/admin/codes/edit/<id>", methods=["GET"])
@login_required
def admin_codes_edit(id):

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))

	c = Code.query.filter_by(id=int(id)).first()

	return render_template("admin/codes/edit.html",
		id=c.id, code=c.code, value=c.value, note=c.note)

@app.route("/admin/stamps/manage", methods=["GET"])
@login_required
def admin_stamps_manage():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/stamps/manage.html")

@app.route("/admin/stamps/edit/<id>", methods=["GET"])
@login_required
def admin_stamps_edit(id):

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))

	s = Stamp.query.filter_by(id=int(id)).first()

	return render_template("admin/stamps/edit.html",
		id=s.id, name=s.name, slots=s.slots, cooldown=s.cooldown//60)

@app.route("/admin/stamps/punches", methods=["GET"])
@login_required
def admin_stamps_punches():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/stamps/punches.html")

@app.route("/admin/rewards/manage", methods=["GET"])
@login_required
def admin_rewards_manage():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/rewards/manage.html")

@app.route("/admin/rewards/edit/<id>", methods=["GET"])
@login_required
def admin_rewards_edit(id):

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))

	r = Reward.query.filter_by(id=int(id)).first()

	return render_template("admin/rewards/edit.html",
		id=r.id, reward=r.reward, value=r.value, stock=r.stock)

@app.route("/admin/rewards/station", methods=["GET"])
@login_required
def admin_rewards_station():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/rewards/station.html")

@app.route("/admin/badgers/manage", methods=["GET"])
@login_required
def admin_badgers_manage():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/badgers/manage.html")

@app.route("/admin/badgers/configure/<id>", methods=["GET"])
@login_required
def admin_badgers_configure(id):

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))

	try:

		b = Badger.query.filter_by(id=int(id)).first()
		return render_template("admin/badgers/configure.html", id=b.id,
			identity=f"{b.identity:08X}", status=b.status, tending=b.tending)

	except:
		pass  # Automatic 404

@app.route("/admin/users/manage", methods=["GET"])
@login_required
def admin_users():

	# Admin only.
	if current_user.type != 1:
		return redirect(url_for("index"))
	return render_template("admin/users/manage.html")

