let lastUpdate = null;

/* Update the table. */
function update()
{
	$.getJSON("/api/user/list", function (data)
	{
		let dataStr = JSON.stringify(data.Users);

		if (lastUpdate != dataStr)
		{
			lastUpdate = dataStr;

			$("#table-data").empty();
			$("#table-data").append(
				"<tr class='table-header'>"+
					"<th style='width: 5em'>UID</th>"+
					"<th>Name</th>"+
					"<th>Email</th>"+
					"<th style='width: 3em'>Points</th>"+
					"<th style='width: 3em'>Actions</th>"+
				"</tr>"
			);

			for (let i = 0; i < data.Users.length; i++)
			{
				$("#table-data").append(
					"<tr id='"+data.Users[i].id+"'>"+
						"<td class='user-contents mono'>"+data.Users[i].uid+"</td>"+
						"<td>"+data.Users[i].name+"</td>"+
						"<td>"+data.Users[i].email+"</td>"+
						"<td>"+data.Users[i].points+"</td>"+
						"<td><center><span class='delete'></span></center></td>"+
					"</tr>"
				);
			}
		}

		setTimeout(update, 1000);
	});
}

$(document).ready(function() { update(); });

/* Given a uid, make a user. */
$("#create-form").submit(function()
{
	$.ajax(
	{
		type: "POST",
		url: "/api/user/create",
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

/* Confirmation dialogue for deleting a user. */
$(document).on("click", ".delete", function()
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
