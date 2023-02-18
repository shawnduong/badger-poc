let lastUpdate = null;

/* Update the table. */
function update()
{
	$.getJSON("/api/reward/list", function (data)
	{
		let dataStr = JSON.stringify(data.Rewards);

		if (lastUpdate != dataStr)
		{
			lastUpdate = dataStr;

			$("#rewards-table").empty();
			$("#rewards-table").append(
				"<tr class='table-header'>"+
					"<th>Reward</th>"+
					"<th style='width: 3em'>Value</th>"+
					"<th style='width: 3em'>Stock</th>"+
					"<th style='width: 3em'>Claims</th>"+
					"<th style='width: 3em'>Actions</th>"+
				"</tr>"
			);

			for (let i = 0; i < data.Rewards.length; i++)
			{
				$("#rewards-table").append(
					"<tr id='"+data.Rewards[i].id+"'>"+
						"<td class='reward-contents'>"+data.Rewards[i].reward+"</td>"+
						"<td>"+data.Rewards[i].value+"</td>"+
						"<td>"+data.Rewards[i].stock+"</td>"+
						"<td>"+data.Rewards[i].claims+"</td>"+
						"<td><center><span class='delete'></span> <span class='edit-icon'></span></center></td>"+
					"</tr>"
				);
			}
		}

		setTimeout(update, 1000);
	});
}

$(document).ready(function() { update(); });

/* Make a reward. */
$("#create-form").submit(function()
{
	$.ajax({
		type: "POST",
		url: "/api/reward/create",
		data: {"reward": $("#reward").val(), "value": $("#value").val(), "stock": $("#stock").val()},
		success: function()
		{
			$("#form-response").html("<span style='color: green;'>Reward "+$("#reward").val()+" created.</span>")
			$("#reward").val("");
			$("#value").val("");
			$("#stock").val("");
		},
		error: function()
		{
			$("#form-response").html("<span style='color: red;'>Action failed.</span>")
		}
	});

	return false;
});

/* Confirmation dialogue for deleting a reward. */
$(document).on("click", ".delete", function()
{
	let tr = $(this).parent().parent().parent();
	let id = tr[0].id;
	let text = tr.find(".reward-contents").text();

	if (!confirm("Are you sure you want to delete "+text+"?"))  return false;

	$.ajax({
		type: "POST",
		url: "/api/reward/delete/"+id,
	});

	return false;
});

/* Edit a reward. */
$(document).on("click", ".edit-icon", function()
{
	let tr = $(this).parent().parent().parent();
	let id = tr[0].id;
	location.href="/admin/rewards/edit/"+id;
});
