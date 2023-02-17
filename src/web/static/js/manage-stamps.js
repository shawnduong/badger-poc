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

			$("#stamps-table-data").empty();
			$("#stamps-table-data:last-child").append(
				"<tr class='table-header'>"+
					"<th>Stamp</th>"+
					"<th style='width: 3em'>Remove</th>"+
				"</tr>"
			);

			for (let i = 0; i < data.Stamps.length; i++)
			{
				$("#stamps-table-data:last-child").append(
					"<tr>"+
						"<td>"+data.Stamps[i].name+"</td>"+
						"<td class='delete' id='"+data.Stamps[i].id+"'></td>"+
					"</tr>"
				);
			}
		}

		setTimeout(update, 1000);
	});
}

$(document).ready(function() { update(); });

/* Make a stamp. */
$("#stamp-create-form").submit(function()
{
	$.ajax({
		type: "POST",
		url: "/api/stamp/create",
		data: {"name": $("#stamp").val()},
		success: function()
		{
			$("#form-response").html("<span style='color: green;'>Stamp "+$("#stamp").val()+" created.</span>")
			$("#stamp").val("");
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
	let text = $(this)[0].previousElementSibling.innerHTML;
	if (!confirm("Are you sure you want to delete "+text+"?"))  return;

	$.ajax({
		type: "POST",
		url: "/api/stamp/delete/"+$(this)[0].id,
	});
});
