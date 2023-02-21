let lastUpdatePending = null;
let lastUpdateApproved = null;
let lastUpdateLocators = null;

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
					"<th style='width: 5em'>Identity</th>"+
					"<th>Mode</th><th>Event</th>"+
					"<th style='width: 6em'>Last Seen</th>"+
					"<th style='width: 3em'>Actions</th>"+
				"</tr>"
			);

			for (let i = 0; i < d.Approved.length; i++)
			{
				let found = "";
				if (d.Approved[i].located == true)
					found = "located";

				$("#approved-table").append(
					"<tr id='"+d.Approved[i].id+"' class='"+found+"'>"+
						"<td class='badger-contents mono'>"+d.Approved[i].identity+"</td>"+
						"<td>"+d.Approved[i].mode+"</td><td>"+d.Approved[i].event+"</td>"+
						"<td>"+to_full_stamp(d.Approved[i].lastSeen * 1000)+"</td>"+
						"<td><center><span class='delete delete-badger'></span> <span class='edit-icon'></span></center></td>"+
					"</tr>"
				);
			}
		}
	});

	$.getJSON("/api/user/locator/list", function (d)
	{
		let dataStr = JSON.stringify(d.Users);

		if (lastUpdateLocators != dataStr)
		{
			lastUpdateLocators = dataStr;

			$("#locator-data").empty();
			$("#locator-data").append(
				"<tr class='table-header'>"+
					"<th>UID</th>"+
					"<th style='width: 3em'>Actions</th>"+
				"</tr>"
			);

			for (let i = 0; i < d.Users.length; i++)
			{
				$("#locator-data").append(
					"<tr id='"+d.Users[i].id+"'>"+
						"<td class='user-contents mono'>"+d.Users[i].uid+"</td>"+
						"<td><center><span class='delete delete-locator'></span></center></td>"+
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

/* Confirm before approving a Badger. */
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

/* Confirm before deleting a Badger. */
$(document).on("click", ".delete-badger", function()
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

/* Configure a Badger. */
$(document).on("click", ".edit-icon", function()
{
	let tr = $(this).parent().parent().parent();
	let id = tr[0].id;
	location.href="/admin/badgers/configure/"+id;
});

/* Given a uid, make a locator. */
$("#create-form").submit(function()
{
	$.ajax(
	{
		type: "POST",
		url: "/api/user/locator/create",
		data: {"uid": $("#uid").val()},
		success: function()
		{
			$("#form-response").html("<span style='color: green;'>User "+$("#uid").val()+" created.</span>")
			$("#uid").val("");
		},
		error: function()
		{
			$("#form-response").html("<span style='color: red;'>Action failed.</span>")
		}
	});

	return false;
});

/* Confirmation dialogue for deleting a locator. */
$(document).on("click", ".delete-locator", function()
{
	let tr = $(this).parent().parent().parent();
	let id = tr[0].id;
	let text = tr.find(".user-contents").text();

	if (!confirm("Are you sure you want to delete "+text+"?"))  return;

	$.ajax(
	{
		type: "POST",
		url: "/api/user/delete/"+id,
	});
});
