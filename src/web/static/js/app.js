let lastUpdatePoints = null;
let lastUpdateAnnouncements = null;
let lastUpdateEvents = null;
let ahidden = true;
let ehidden = true;

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

	$.getJSON("/api/event/list", function (data)
	{
		let dataStr = JSON.stringify(data.Events);

		if (lastUpdateEvents != dataStr)
		{
			var e = data.Events;
			e.reverse();
			lastUpdateEvents = dataStr;

			$("#events-table-data").empty();
			$("#events-table-data").append(
				"<tr class='table-header'>"+
					"<th style='width: 7em'>Time</th>"+
					"<th style='width: 4em'>Length</th>"+
					"<th style='width: 4em'>Location</th>"+
					"<th>Title</th>"+
				"<th style='width: 3em'>Info</th>"
			);

			let active = 0;
			let hidden = 0;

			for (let i = 0; i < e.length; i++)
			{
				let t = new Date(e[i].start * 1000);
				let dateStr = t.toLocaleDateString().slice(0, -5);
				let timeStr = t.toLocaleTimeString().slice(0, -6) + t.toLocaleTimeString().slice(-2);
				let stat = "";
				let vis = "";

				if (e[i].status == 2)
				{
					stat = "event-completed eextra";
					vis = "hidden";
					hidden++;
				}
				else if (e[i].status == 1)
				{
					stat = "event-happening";
					active++;
				}
				else
				{
					/* Only 5 shown at once max. */
					if (active >= 5)
					{
						stat = "eextra";
						vis = "hidden";
						hidden++;
					}
					else
					{
						stat = "";
						active++;
					}
				}

				$("#events-table-data").append(
					"<tr id='"+e[i].id+"' class='"+stat+"' "+vis+">" +
						"<td>"+dateStr+" "+timeStr+"</td>"+
						"<td>"+e[i].length+"</td>"+
						"<td>"+e[i].location+"</td>"+
						"<td class='event-title'>"+e[i].title+"</td>"+
						"<td><center><h3><a class='nodecor' href='/event/"+e[i].id+
							"'>&gt;&gt;</a></h3></center></td>"+
					"</tr>"
				);
			}

			if (hidden > 0)  $("#events-expand-toggle").attr("hidden", false);
			else             $("#events-expand-toggle").attr("hidden", true);
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
		$("#announcements-expand-toggle").text("Collapse");
	}
	else
	{
		ahidden = true;
		$(".aextra").each(function () { $(this).attr("hidden", true) });
		$("#announcements-expand-toggle").text("Expand");
	}
});

/* Un/hide events. */
$("#events-expand-toggle").click(function()
{
	if (ehidden)
	{
		ehidden = false;
		$(".eextra").each(function () { $(this).attr("hidden", false) });
		$("#events-expand-toggle").text("Collapse");
	}
	else
	{
		ehidden = true;
		$(".eextra").each(function () { $(this).attr("hidden", true) });
		$("#events-expand-toggle").text("Expand");
	}
});
