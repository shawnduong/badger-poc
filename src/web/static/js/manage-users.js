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
			console.log("Updating");

			$("#user-table-data ").empty();
			$("#user-table-data:last-child").append(
				"<tr class='table-header'>"+
					"<th>Card ID</th>"+
					"<th>Name</th>"+
					"<th>Email</th>"+
					"<th>Points</th>"+
					"<th>Remove</th>"+
				"</tr>"
			);

			for (let i = 0; i < data.Users.length; i++)
			{
				$("#user-table-data:last-child").append(
					"<tr>"+
						"<td>"+data.Users[i].cardID+"</td>"+
						"<td>"+data.Users[i].name+"</td>"+
						"<td>"+data.Users[i].email+"</td>"+
						"<td>"+data.Users[i].points+"</td>"+
						"<td class='delete' id='"+data.Users[i].cardID+"'></td>"+
					"</tr>"
				);
			}
		}

		setTimeout(update, 1000);
	});
}

$(document).ready(function() { update(); });

/* Given a cardID, make a user. */
$("#user-create-form").submit(function()
{
	$.ajax({
		type: "POST",
		url: "/api/user/create",
		data: {"cardID": $("#cardID").val()},
		success: function() {
			$("#form-response").html("<span style='color: green;'>User "+$("#cardID").val()+" created.</span>")
			$("#cardID").val("");
		},
		error: function() {
			$("#form-response").html("<span style='color: red;'>Action failed.</span>")
		}
	});

	return false;
});

/* Confirmation dialogue for deleting a user. */
$(document).on("click", ".delete", function()
{
	if (!confirm("Are you sure you want to delete "+$(this)[0].id+"?"))  return;

	$.ajax({
		type: "POST",
		url: "/api/user/delete/"+$(this)[0].id,
	});
});
