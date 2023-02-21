let lastUpdate = null;

/* Update the table. */
function update()
{
	$.getJSON("/api/stamp/list", function (data)
	{
		let dataStr = JSON.stringify(data.Stamps);

		if (lastUpdate != dataStr)
		{
			lastUpdate = dataStr;

			$("#stamps-table").empty();
			$("#stamps-table").append(
				"<tr class='table-header'>"+
					"<th>Stamp</th>"+
					"<th style='width: 3em'>Slots</th>"+
					"<th style='width: 3em'>Cooldown</th>"+
					"<th style='width: 3em'>Actions</th>"+
				"</tr>"
			);

			for (let i = 0; i < data.Stamps.length; i++)
			{
				$("#stamps-table").append(
					"<tr id='"+data.Stamps[i].id+"'>"+
						"<td class='stamp-name'>"+data.Stamps[i].name+"</td>"+
						"<td>"+data.Stamps[i].slots+"</td>"+
						"<td>"+data.Stamps[i].cooldown+"</td>"+
						"<td><center><span class='delete'></span> <span class='edit-icon'></span></center></td>"+
					"</tr>"
				);
			}
		}

		setTimeout(update, 1000);
	});
}

$(document).ready(function() { update(); });

/* Make a stamp. */
$("#create-form").submit(function()
{
	$.ajax({
		type: "POST",
		url: "/api/stamp/create",
		data: {"name": $("#stamp").val(), "slots": $("#slots").val(), "cooldown": $("#cooldown").val()},
		success: function()
		{
			$("#form-response").html("<span style='color: green;'>Stamp "+$("#stamp").val()+" created.</span>")
			$("#stamp").val("");
			$("#slots").val("");
			$("#cooldown").val("");
		},
		error: function()
		{
			$("#form-response").html("<span style='color: red;'>Action failed.</span>")
		}
	});

	return false;
});

/* Confirmation dialogue for deleting a stamp. */
$(document).on("click", ".delete", function()
{
	let tr = $(this).parent().parent().parent();
	let id = tr[0].id;
	let text = tr.find(".stamp-name").text();

	if (!confirm("Are you sure you want to delete "+text+"?"))  return false;

	$.ajax({
		type: "POST",
		url: "/api/stamp/delete/"+id,
	});

	return false;
});

/* Edit a stamp. */
$(document).on("click", ".edit-icon", function()
{
	let tr = $(this).parent().parent().parent();
	let id = tr[0].id;
	location.href="/admin/stamps/edit/"+id;
});
