import bcrypt
import time

from app import *

from flask_login import LoginManager, login_required, login_user, logout_user, current_user

# If there is no admin account, make a default one.
if Account.query.filter_by(name="admin", type=1).first() == None:
	admin = Account(1, "password", None, "admin", None, None)
	db.session.add(admin)
	db.session.commit()

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"

@loginManager.user_loader
def load_user(id: int):
	return Account.query.get(id)

@app.route("/login", methods=["POST"])
def login():

	# Passwordless UID based login.
	user = Account.get_user(request.form["uid"])

	if user == False:
		time.sleep(1)  # Prevent brute.
		return render_template("index.html", failed=True)

	login_user(user)
	return redirect(url_for("application"))

@app.route("/admin/login", methods=["POST"])
def login_admin():

	# Password based login.
	user = Account.login(request.form["username"], request.form["password"])

	if user == False:
		time.sleep(1)  # Prevent brute.
		return render_template("admin_login.html", failed=True)

	login_user(user)
	return redirect(url_for("admin"))

@app.route("/admin/password/change", methods=["POST"])
@login_required
def admin_password_change_api():

	try:
		assert bcrypt.checkpw(request.form["password-current"].encode(), current_user.password)
		assert request.form["password-new"] == request.form["password-confirm"]
	except:
		return render_template("admin/password/change.html", failed=True)

	current_user.password = bcrypt.hashpw(request.form["password-new"].encode(), bcrypt.gensalt(4))
	db.session.commit()

	return redirect(url_for("admin"))

@app.route("/logout", methods=["GET"])
@login_required
def logout():

	if current_user.type == 1:
		logout_user()
		return render_template("admin/login.html")
	else:
		logout_user()
		return render_template("index.html")

