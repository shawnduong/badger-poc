from app import *

from flask_login import current_user, login_required

@app.route("/app", methods=["GET"])
@login_required
def application():

	# Admin redirect to admin panel.
	if current_user.type == 1:
		return redirect(url_for("admin"))
	return render_template("app.html")

