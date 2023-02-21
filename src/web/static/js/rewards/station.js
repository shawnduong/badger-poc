let lastUpdateRedemptions = null;

function load_redemptions()
{
	$.getJSON("/api/reward/redemption/list", function (d)
	{
		let dataStr = JSON.stringify(d.Redemptions);

		if (dataStr != lastUpdateRedemptions)
		{
			lastUpdateRedemptions = dataStr;

			$("#redemption-table").empty();
			$("#redemption-table").append(
				"<tr class='table-header'>"+
					"<th style='width: 4em'>UID</th>"+
					"<th style='width: 4em'>Name</th>"+
					"<th>Reward</th>"+
				"<th style='width: 3em'>Actions</th>"
			);

			for (let i = 0; i < d.Redemptions.length; i++)
			{
				let r = d.Redemptions[i];
				$("#redemption-table").append(
					"<tr id='"+r.id+"'>"+
						"<td>"+r.uid+"</td><td>"+r.name+"</td><td>"+r.reward+"</td>"+
						"<td><center><span class='delete'></span></center></td>"+
					"</tr>"
				);
			}
		}
	});
}
function load_redemptions_loop()
{
	load_redemptions();
	setTimeout(load_redemptions_loop, 5000);
}

/* Confirm before deleting a redemption. */
$(document).on("click", ".delete", function()
{
	let tr = $(this).parent().parent().parent();
	let id = tr[0].id;

	if (!confirm("Are you sure you want to delete this redemption?"))  return;

	$.ajax(
	{
		type: "POST",
		url: "/api/reward/redemption/delete/"+id,
		success: function()
		{
			location.href="/admin/rewards/station";
		},
		error: function()
		{
			alert("Unexpected error occurred.");
		}
	});
});
