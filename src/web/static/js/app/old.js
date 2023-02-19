let lastUpdateInfo = null;
let lastUpdatePoints = null;
let lastUpdateAnnouncements = null;
let lastUpdateEvents = null;
let lastUpdateStamps = null;
let ahidden = true;
let ehidden = true;

/* Continuously update the page via AJAX. */
function refresh()
{
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

	$.getJSON("/api/stamp/list", function (data)
	{
		let dataStr = JSON.stringify(data.Stamped+data.Unstamped);

		if (lastUpdateStamps != dataStr)
		{
			lastUpdateStamps = data.Stamped+data.Unstamped;

			$("#stamped").empty();
			$("#unstamped").empty();

			for (let i = 0; i < data.Stamped.length; i++)
			{
				$("#stamped").append(
					"<input type='checkbox' onclick='return false' checked>"+
						data.Stamped[i]+
					"</input><br>"
				);
			}

			for (let i = 0; i < data.Unstamped.length; i++)
			{
				$("#unstamped").append(
					"<input type='checkbox' onclick='return false'>"+
						data.Unstamped[i]+
					"</input><br>"
				);
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
