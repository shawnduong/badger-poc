/* Load announcements from /api/announcement/list into #announcement-table. Load
   up to n announcements and hide the rest. If n is negative, don't hide. */
function load_announcements(n)
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
