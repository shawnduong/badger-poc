import bcrypt
import time

from app import *

from flask_login import LoginManager, login_required, login_user, logout_user, current_user

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"

@loginManager.user_loader
def load_user(id: int):
	return Account.query.get(id)

@app.route("/login", methods=["POST"])
def login():

	user = Account.get_user(request.form["cardID"])

	if user == False:
		time.sleep(1)  # Prevent brute.
		return render_template("index.html", failed=True)

	login_user(user)
	return redirect(url_for("application"))

@app.route("/admin/login", methods=["POST"])
def login_admin():

	user = Account.login(request.form["username"], request.form["password"])

	if user == False:
		time.sleep(1)  # Prevent brute.
		return render_template("admin_login.html", failed=True)

	login_user(user)
	return redirect(url_for("admin"))

@app.route("/admin/change-password", methods=["POST"])
@login_required
def change_password_admin():

	if not bcrypt.checkpw(request.form["curr-password"].encode(), current_user.password):
		return render_template("admin/change-password.html", failed=True)

	if request.form["new-password"] != request.form["conf-password"]:
		return render_template("admin/change-password.html", failed=True)

	current_user.password = bcrypt.hashpw(request.form["new-password"].encode(),
		bcrypt.gensalt(4))
	db.session.commit()

	return redirect(url_for("admin"))

@app.route("/logout", methods=["GET"])
@login_required
def logout():

	if current_user.acctType == 1:
		logout_user()
		return render_template("admin/login.html")
	else:
		logout_user()
		return render_template("index.html")

