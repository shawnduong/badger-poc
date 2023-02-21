let lastUpdatePunches = null;

/* Load events from /api/stamp/punch/list into #punch-table. */
function load_punches()
{
	$.getJSON("/api/stamp/punch/list", function (d)
	{
		let dataStr = JSON.stringify(d.Punches);

		if (lastUpdatePunches != dataStr)
		{
			lastUpdatePunches = dataStr;

			$("#punch-table").empty();

			$("#punch-table").append(
				"<tr class='table-header'>"+
					"<th style='width: 4em'>UID</th>"+
					"<th style='width: 4em'>Name</th>"+
					"<th>Stamp</th>"+
				"<th style='width: 3em'>Actions</th>"
			);

			for (let i = 0; i < d.Punches.length; i++)
			{
				let p = d.Punches[i];
				$("#punch-table").append(
					"<tr id='"+p.id+"'>"+
						"<td>"+p.uid+"</td><td>"+p.name+"</td><td>"+p.stamp+"</td>"+
						"<td><center><span class='delete'></span></center></td>"+
					"</tr>"
				);
			}
		}
	});
}
function load_punches_loop()
{
	load_punches();
	setTimeout(load_punches_loop, 5000);
}

/* Confirm before deleting a punch. */
$(document).on("click", ".delete", function()
{
	let tr = $(this).parent().parent().parent();
	let id = tr[0].id;

	if (!confirm("Are you sure you want to delete this punch?"))  return;

	$.ajax(
	{
		type: "POST",
		url: "/api/stamp/punch/delete/"+id,
		success: function()
		{
			location.href="/admin/stamps/punches";
		},
		error: function()
		{
			alert("Unexpected error occurred.");
		}
	});
});
