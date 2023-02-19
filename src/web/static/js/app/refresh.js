let lastUpdateInfo = null;

function update_user_info()
{
	$.getJSON("/api/user/info", function (data)
	{
		let dataStr = JSON.stringify(data.User);

		if (lastUpdateInfo != dataStr)
		{
			lastUpdateInfo = dataStr;

			if (data.User.name == null) data.User.name = "Not set";
			if (data.User.email == null) data.User.email = "Not set";

			$("#info-uid").text(data.User.uid);
			$("#info-name").text(data.User.name);
			$("#info-email").text(data.User.email);
			$("#info-points").text(data.User.points);
		}
	});
}

/* Continuously update the page via AJAX. */
function refresh()
{
	update_user_info();
}
function refresh_loop()
{
	refresh();
	setTimeout(refresh_loop, 5000);
}
