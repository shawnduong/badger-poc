let lastUpdateAnnouncements = null;

/* Load announcements from /api/announcement/list into #announcement-table. */
function load_announcements()
{
	$.getJSON("/api/announcement/list", function (d)
	{
		for (let i = d.Announcements.length-1; i >= 0; i--)
		{
			let t = to_stamp(d.Announcements[i].timestamp);
			$("#announcement-table").append(
				"<tr id='"+d.Announcements[i].id+"'>" +
					"<td>"+t+"</td>"+
					"<td class='announcement-contents'>"+d.Announcements[i].contents+"</td>"+
					"<td><center><span class='delete'></span> <span class='edit-icon'></span></center></td>"+
				"</tr>"
			);
		}
	});
}

/* Load announcements from /api/announcement/list into #announcement-list. */
function load_announcementsl()
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
				let time = to_stamp(t);
				$("#announcements-list").append("<p><b>"+time+"</b> "+a[i].contents+"</p><hr>");
			}

			for (let i = 3; i < a.length; i++)
			{
				let t = new Date(a[i].timestamp);
				let time = to_stamp(t);
				if (ahidden)  $("#announcements-list").append("<p class='aextra' hidden><b>"+time+"</b> "+a[i].contents+"</p><hr>");
				else          $("#announcements-list").append("<p class='aextra'><b>"+time+"</b> "+a[i].contents+"</p><hr>");
			}
		}
	});
}
