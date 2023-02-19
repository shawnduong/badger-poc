let lastUpdateInfo = null;
let lastUpdatePoints = null;
let lastUpdateAnnouncements = null;
let lastUpdateEvents = null;
let lastUpdateStamps = null;
let ahidden = true;
let ehidden = true;

/* Continuously update the page via AJAX. */
function refresh()
{

	$.getJSON("/api/stamp/list", function (data)
	{
		let dataStr = JSON.stringify(data.Stamped+data.Unstamped);

		if (lastUpdateStamps != dataStr)
		{
			lastUpdateStamps = data.Stamped+data.Unstamped;

			$("#stamped").empty();
			$("#unstamped").empty();

			for (let i = 0; i < data.Stamped.length; i++)
			{
				$("#stamped").append(
					"<input type='checkbox' onclick='return false' checked>"+
						data.Stamped[i]+
					"</input><br>"
				);
			}

			for (let i = 0; i < data.Unstamped.length; i++)
			{
				$("#unstamped").append(
					"<input type='checkbox' onclick='return false'>"+
						data.Unstamped[i]+
					"</input><br>"
				);
			}
		}
	});
};
function refresh_loop()
{
	refresh();
	setTimeout(refresh_loop, 5000);
};

$(document).ready(function() { refresh_loop(); });
