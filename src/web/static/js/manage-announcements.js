/* Load announcements. */
$(document).ready(function()
{
	$.getJSON("/api/announcement/list", function (data)
	{
		for (let i = data.Announcements.length-1; i >= 0; i--)
		{
			let t = new Date(data.Announcements[i].timestamp);
			$("#announcement-table-data").append(
				"<tr id='"+data.Announcements[i].id+"'>" +
					"<td>"+t.toLocaleDateString()+"<br>"+t.toLocaleTimeString()+"</td>"+
					"<td class='announcement-contents'>"+data.Announcements[i].contents+"</td>"+
					"<td><center><span class='delete'></span> <span class='edit-icon'></center></td>"+
				"</tr>"
			);
		}
	});
});

/* Confirm before deleting an announcement. */
$(document).on("click", ".delete", function()
{
	id = $(this).parent().parent().parent()[0].id;
	text = $(this).parent().parent().parent().find(".announcement-contents").text().slice(0, 24)+"...";
	if (!confirm("Are you sure you want to delete \""+text+"\"?"))  return;

	$.ajax({
		type: "POST",
		url: "/api/announcement/delete/"+id,
		success: function()
		{
			location.href="/admin/announcements/manage";
		},
		error: function()
		{
			alert("Unexpected error occurred.");
		}
	});
});
