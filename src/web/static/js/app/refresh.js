let lastUpdateInfo = null;

function update_rewards(rewards)
{
	$("#rewards").empty();
	$("#rewards").append(
		"<tr class='table-header'>"+
			"<th>Item</th>"+
			"<th style='width: 3em'>Points</th>"+
			"<th style='width: 3em'>Stock</th>"+
			"<th style='width: 3em'>Status</th>"+
			"<th style='width: 3em'>Redeem</th>"+
		"</tr>"
	);

	for (let i = 0; i < rewards.length; i++)
	{
		let str = "<tr id='"+rewards[i].id+"'>"+
			"<td class='reward-contents'>"+rewards[i].reward+"</td>"+
			"<td class='reward-value'>"+rewards[i].value+"</td>"+
			"<td>"+rewards[i].stock+"</td>";

		if (rewards[i].status == 2)
			str += "<td>✔✔</td>";
		else if (rewards[i].status == 1)
			str += "<td>✔</td>";
		else
			str += "<td></td>";

		str += "<td class='claim hovercursor'><center><h3 style='color: #F4A460'>&gt;&gt;</center></h3></td>";
		str += "</tr>";

		$("#rewards").append(str);
	}
}

function update_stamps(stamps)
{
	$("#stamps").empty();

	for (let i = 0; i < stamps.length; i++)
	{
		let str = "<tr><td>"+stamps[i].name+"</td><td>";

		for (let j = 0; j < stamps[i].slots; j++)
		{
			if (j < stamps[i].punches)
				str += "★";
			else
				str += "☆";
		}

		str += "</td></tr>";

		$("#stamps").append(str);
	}
}

function update_user_info()
{
	$.getJSON("/api/user/info", function (data)
	{
		let dataStr = JSON.stringify(data.User);

		if (lastUpdateInfo != dataStr)
		{
			lastUpdateInfo = dataStr;

			if (data.User.name == null) data.User.name = "Not set";
			if (data.User.email == null) data.User.email = "Not set";

			$("#info-uid").text(data.User.uid);
			$("#info-name").text(data.User.name);
			$("#info-email").text(data.User.email);
			$("#info-points").text(data.User.points);

			update_stamps(data.User.stamps);
			update_rewards(data.User.rewards);

			$("#badge-breakdown").empty();

			for (let i = 0; i < data.User.breakdown.length; i++)
			{
				$("#badge-breakdown").append("<li>"+data.User.breakdown[i]+"</li>");
			}
		}
	});
}

/* Continuously update the page via AJAX. */
function refresh()
{
	update_user_info();
	load_announcementsl();
	load_events(false);
}
function refresh_loop()
{
	refresh();
	setTimeout(refresh_loop, 5000);
}
