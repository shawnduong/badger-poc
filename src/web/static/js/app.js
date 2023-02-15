let lastUpdatePoints = null;
let lastUpdateAnnouncements = null;
let ahidden = true;

/* Continuously update the page via AJAX. */
function refresh()
{
	$.getJSON("/api/user/info", function (data)
	{
		if (data.User.name == null) data.User.name = "Not set";
		if (data.User.email == null) data.User.email = "Not set";
		$("#name").text(data.User.name);
		$("#email").text(data.User.email);
	});

	$.getJSON("/api/announcement/list", function (data)
	{
		let dataStr = JSON.stringify(data.Announcements);

		if (lastUpdateAnnouncements != dataStr)
		{
			let a = data.Announcements;
			a.reverse();
			lastUpdateAnnouncements = dataStr;

			$("#announcements-list").empty();

			if (a.length <= 3)  $("#announcements-expand-toggle").attr("hidden", true);
			else                $("#announcements-expand-toggle").attr("hidden", false);

			for (let i = 0; i < 3; i++)
			{
				if (i == a.length)  break;

				let t = new Date(a[i].timestamp);
				let time = t.toLocaleDateString().slice(0, -5)+" "+
					t.toLocaleTimeString().slice(0, -6)+t.toLocaleTimeString().slice(-2);
				$("#announcements-list").append("<p><b>"+time+"</b> "+a[i].contents+"</p>");
			}

			for (let i = 3; i < a.length; i++)
			{
				let t = new Date(a[i].timestamp);
				let time = t.toLocaleDateString().slice(0, -5)+" "+
					t.toLocaleTimeString().slice(0, -6)+t.toLocaleTimeString().slice(-2);
				if (ahidden)  $("#announcements-list").append("<p class='aextra' hidden><b>"+time+"</b> "+a[i].contents+"</p>");
				else          $("#announcements-list").append("<p class='aextra'><b>"+time+"</b> "+a[i].contents+"</p>");
			}
		}
	});
};
function refresh_loop()
{
	refresh();
	setTimeout(refresh_loop, 5000);
};

$(document).ready(function() { refresh_loop(); });

/* Name change dialogue. */
$("#edit-name").click(function()
{
	$("#name-container").attr("hidden", true);
	$("#name-edit-container").attr("hidden", false);
});
$("#name-edit-cancel").click(function()
{
	$("#name-container").attr("hidden", false);
	$("#name-edit-container").attr("hidden", true);
});
$("#name-edit-form").submit(function()
{
	$.ajax({
		type: "POST",
		url: "/api/user/edit/name",
		data: {"name": $("#name-form").val()},
		success: function()
		{
			refresh();
			$("#name-container").attr("hidden", false);
			$("#name-edit-container").attr("hidden", true);
		}
	});

	return false;
});

/* Email change dialogue. */
$("#edit-email").click(function()
{
	$("#email-container").attr("hidden", true);
	$("#email-edit-container").attr("hidden", false);
});
$("#email-edit-cancel").click(function()
{
	$("#email-container").attr("hidden", false);
	$("#email-edit-container").attr("hidden", true);
});
$("#email-edit-form").submit(function()
{
	$.ajax({
		type: "POST",
		url: "/api/user/edit/email",
		data: {"email": $("#email-form").val()},
		success: function()
		{
			refresh();
			$("#email-container").attr("hidden", false);
			$("#email-edit-container").attr("hidden", true);
		}
	});

	return false;
});

/* Un/hide announcements. */
$("#announcements-expand-toggle").click(function()
{
	if (ahidden)
	{
		ahidden = false;
		$(".aextra").each(function () { $(this).attr("hidden", false) });
		$("#announcements-expand-toggle").text("Unexpand");
	}
	else
	{
		ahidden = true;
		$(".aextra").each(function () { $(this).attr("hidden", true) });
		$("#announcements-expand-toggle").text("Expand");
	}
});
