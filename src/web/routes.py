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

	if current_user.acctType == 1:
		return redirect(url_for("admin"))
	return render_template("app.html")

@app.route("/admin/login", methods=["GET"])
def admin_login():

	if current_user.is_authenticated:
		return redirect(url_for("admin"))
	return render_template("admin/login.html")

@app.route("/admin", methods=["GET"])
@login_required
def admin():

	if current_user.acctType != 1:
		return redirect(url_for("index"))
	return render_template("admin/admin.html")

@app.route("/admin/change-password", methods=["GET"])
@login_required
def admin_change_password():

	if current_user.acctType != 1:
		return redirect(url_for("index"))
	return render_template("admin/change-password.html")

@app.route("/admin/announcements/manage", methods=["GET"])
@login_required
def admin_announcements_manage():

	if current_user.acctType != 1:
		return redirect(url_for("index"))
	return render_template("admin/announcements/manage.html")

@app.route("/admin/announcements/create", methods=["GET"])
@login_required
def admin_announcements_create():

	if current_user.acctType != 1:
		return redirect(url_for("index"))
	return render_template("admin/announcements/create.html")

@app.route("/admin/users", methods=["GET"])
@login_required
def admin_users():

	if current_user.acctType != 1:
		return redirect(url_for("index"))
	return render_template("admin/users.html")

