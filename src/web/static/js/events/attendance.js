let lastUpdateAttendances = null;

/* Load events from /api/event/attendance/list into #attendance-table. */
function load_attendances()
{
	$.getJSON("/api/event/attendance/list", function (d)
	{
		let dataStr = JSON.stringify(d.Attendances);

		if (lastUpdateAttendances != dataStr)
		{
			lastUpdateAttendances = dataStr;

			$("#attendance-table").empty();

			$("#attendance-table").append(
				"<tr class='table-header'>"+
					"<th style='width: 4em'>UID</th>"+
					"<th style='width: 4em'>Name</th>"+
					"<th>Event</th>"+
				"<th style='width: 3em'>Actions</th>"
			);

			for (let i = 0; i < d.Attendances.length; i++)
			{
				let a = d.Attendances[i];
				$("#attendance-table").append(
					"<tr id='"+a.id+"'>"+
						"<td>"+a.uid+"</td><td>"+a.name+"</td><td>"+a.event+"</td>"+
						"<td><center><span class='delete'></span></center></td>"+
					"</tr>"
				);
			}
		}
	});
}
function load_attendances_loop()
{
	load_attendances();
	setTimeout(load_attendances_loop, 5000);
}

/* Confirm before deleting an attendance. */
$(document).on("click", ".delete", function()
{
	let tr = $(this).parent().parent().parent();
	let id = tr[0].id;

	if (!confirm("Are you sure you want to delete this attendance?"))  return;

	$.ajax(
	{
		type: "POST",
		url: "/api/event/attendance/delete/"+id,
		success: function()
		{
			location.href="/admin/events/attendances";
		},
		error: function()
		{
			alert("Unexpected error occurred.");
		}
	});
});
