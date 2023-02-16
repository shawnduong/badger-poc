let lastUpdate = null;

/* Update the table. */
function update()
{
	$.getJSON("/api/code/list", function (data)
	{
		let dataStr = JSON.stringify(data.Codes);

		if (lastUpdate != dataStr)
		{
			lastUpdate = dataStr;

			$("#codes-table-data").empty();
			$("#codes-table-data:last-child").append(
				"<tr class='table-header'>"+
					"<th style='width: 8em'>Code</th>"+
					"<th style='width: 3em'>Value</th>"+
					"<th>Note</th>"+
					"<th style='width: 3em'>Remove</th>"+
				"</tr>"
			);

			for (let i = 0; i < data.Codes.length; i++)
			{
				$("#codes-table-data:last-child").append(
					"<tr>"+
						"<td>"+data.Codes[i].code+"</td>"+
						"<td>"+data.Codes[i].value+"</td>"+
						"<td>"+data.Codes[i].note+"</td>"+
						"<td class='delete' id='"+data.Codes[i].id+"'></td>"+
					"</tr>"
				);
			}
		}

		setTimeout(update, 1000);
	});
}

$(document).ready(function() { update(); });

/* Make a code. */
$("#code-create-form").submit(function()
{
	$.ajax({
		type: "POST",
		url: "/api/code/create",
		data: {"code": $("#code").val(), "value": $("#value").val(), "note": $("#note").val()},
		success: function()
		{
			$("#form-response").html("<span style='color: green;'>Code "+$("#code").val()+" created.</span>")
			$("#code").val("");
			$("#value").val("");
			$("#note").val("");
		},
		error: function()
		{
			$("#form-response").html("<span style='color: red;'>Action failed.</span>")
		}
	});

	return false;
});

/* Confirmation dialogue for deleting a code. */
$(document).on("click", ".delete", function()
{
	let text = $(this)[0].previousElementSibling.previousElementSibling.previousElementSibling.innerHTML;
	if (!confirm("Are you sure you want to delete "+text+"?"))  return;

	$.ajax({
		type: "POST",
		url: "/api/code/delete/"+$(this)[0].id,
	});
});
