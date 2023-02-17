from app import *

from flask_login import current_user, login_required

@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET"])
def index():

	if current_user.is_authenticated:
		return redirect(url_for("application"))
	return render_template("index.html")

