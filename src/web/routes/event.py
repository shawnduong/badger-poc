from app import *
from func.timemath import to_hm

from flask_login import current_user, login_required

@app.route("/event/<id>", methods=["GET"])
@login_required
def event(id):

	if current_user.type == 1:
		backlink = "/admin/events/manage"
	else:
		backlink = "/app"

	try:

		e = Event.query.filter_by(id=int(id)).first()

		return render_template("event.html",
			backlink=backlink,
			title=e.title,
			author=e.author,
			location=e.room,
			start=e.start,
			duration=to_hm(e.duration),
			points=e.points,
			weblink=e.weblink,
			description=e.description
		)

	except:
		pass  # Automatic 404

