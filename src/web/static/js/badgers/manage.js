let lastUpdate = null;

function update_tables()
{
	$.getJSON("/api/badger/list", function (d)
	{
		let dataStr = JSON.stringify(d.Pending);

		if (lastUpdate != dataStr)
		{
			lastUpdate = dataStr;

			$("#pending-table").empty();
			$("#approved-table").empty();

			for (let i = 0; i < d.Pending.length; i++)
			{
				$("#pending-table").append(
					"<tr id='"+d.Pending[i].id+"'>"+
						"<td class='badger-contents mono'>"+d.Pending[i].identity+"</td>"+
						"<td class='confirm'></td>"+
					"</tr>"
				);
			}

			$("#approved-table").append(
				"<tr class='table-header'>"+
					"<th style='width: 5em'>UID</th>"+
					"<th>Mode</th><th>Event</th>"+
					"<th>Actions</th>"+
				"</tr>"
			);

			for (let i = 0; i < d.Approved.length; i++)
			{
				$("#approved-table").append(
					"<tr id='"+d.Approved[i].id+"'>"+
						"<td class='badger-contents mono'>"+d.Approved[i].identity+"</td>"+
						"<td>"+d.Approved[i].mode+"</td><td>"+d.Approved[i].event+"</td>"+
						"<td class='delete'></td>"+
					"</tr>"
				);
			}
		}
	});
}
function update_tables_loop()
{
	update_tables();
	setTimeout(update_tables_loop, 1000);
}

$(document).on("click", ".confirm", function()
{
	let tr = $(this).parent();
	let id = tr[0].id;
	let text = tr.find(".badger-contents").text();

	if (!confirm("Are you sure you want to approve "+text+"?"))  return false;

	$.ajax(
	{
		type: "POST",
		url: "/api/badger/approve/"+id,
		success: function()
		{
			update_tables();
		},
		error: function()
		{
			alert("Unexpected error occurred.");
		}
	});

	return false;
});
