let lastUpdatePending = null;
let lastUpdateApproved = null;

function update_tables()
{
	$.getJSON("/api/badger/list", function (d)
	{
		let dataStrPending = JSON.stringify(d.Pending);
		let dataStrApproved = JSON.stringify(d.Approved);

		if ((lastUpdatePending != dataStrPending) || (lastUpdateApproved != dataStrApproved))
		{
			lastUpdatePending = dataStrPending;
			lastUpdateApproved = dataStrApproved;

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
					"<th style='width: 6em'>Last Seen</th>"+
					"<th style='width: 3em'>Actions</th>"+
				"</tr>"
			);

			for (let i = 0; i < d.Approved.length; i++)
			{
				$("#approved-table").append(
					"<tr id='"+d.Approved[i].id+"'>"+
						"<td class='badger-contents mono'>"+d.Approved[i].identity+"</td>"+
						"<td>"+d.Approved[i].mode+"</td><td>"+d.Approved[i].event+"</td>"+
						"<td>"+to_full_stamp(d.Approved[i].lastSeen * 1000)+"</td>"+
						"<td><center><span class='delete'></span> <span class='edit-icon'></span></center></td>"+
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

$(document).on("click", ".delete", function()
{
	let tr = $(this).parent().parent().parent();
	let id = tr[0].id;
	let text = tr.find(".badger-contents").text();

	if (!confirm("Are you sure you want to delete "+text+"?"))  return false;

	$.ajax(
	{
		type: "POST",
		url: "/api/badger/delete/"+id,
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
