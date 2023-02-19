let lastUpdateEvents = null;

/* Load events from /api/event/list into #event-table. */
function load_events(admin)
{
	$.getJSON("/api/event/list", function (d)
	{
		let dataStr = JSON.stringify(d.Events);

		if (lastUpdateEvents != dataStr)
		{
			lastUpdateEvents = dataStr;

			$("#event-table").empty();

			let str =
				"<tr class='table-header'>"+
					"<th style='width: 7em'>Time</th>"+
					"<th style='width: 4em'>Length</th>"+
					"<th style='width: 4em'>Location</th>"+
					"<th>Title</th>"+
					"<th style='width: 3em'>Info</th>";

			if (admin)
			{
				str += "<th style='width: 3em'>Actions</th>";
			}

			str += "</tr>";

			$("#event-table").append(str);

			let active = 0;
			let hidden = 0;

			for (let i = d.Events.length-1; i >= 0; i--)
			{
				let t = to_stamp(d.Events[i].start * 1000);
				let stat = "";
				let vis = "";

				if (d.Events[i].status == 2)
					stat = "event-completed";
				else if (d.Events[i].status == 1)
					stat = "event-happening";
				else
					stat = "";

				if (!admin)
				{
					if (d.Events[i].status == 2)
					{
						stat += " eextra";
						vis = "hidden";
						hidden++;
					}
					else if (d.Events[i].status == 1)
					{
						active++;
					}
					else
					{
						/* Only 5 shown at once max. */
						if (active >= 5)
						{
							stat += " eextra";
							vis = "hidden";
							hidden++;
						}
						else  active++;
					}
				}

				str =
					"<tr id='"+d.Events[i].id+"' class='"+stat+"' "+vis+">" +
						"<td>"+t+"</td>"+
						"<td>"+d.Events[i].length+"</td>"+
						"<td>"+d.Events[i].location+"</td>"+
						"<td class='event-title'>"+d.Events[i].title+"</td>"+
						"<td><center><h3><a class='nodecor' href='/event/"+d.Events[i].id+
							"'>&gt;&gt;</a></h3></center></td>";

				if (admin)
				{
					str +=
						"<td><center><span class='delete'></span> <span class='edit-icon'>"+
							"</span></center></td>";
				}

				str += "</tr>";

				$("#event-table").append(str);
			}

			if (!admin)
			{
				if (hidden > 0)  $("#events-expand-toggle").attr("hidden", false);
				else             $("#events-expand-toggle").attr("hidden", true);
			}
		}
	});
}

/* Event preview. */
function update_preview()
{
	let title = $("#title").val();
	let author = $("#author").val();
	let locate = $("#location").val();
	let start = $("#start").val();
	let durationH = $("#duration-hours").val();
	let durationM = $("#duration-minutes").val();
	let points = $("#pts").val();
	let link = $("#weblink").val();
	let description = $("#description").val();
	let lengthStr = to_HhMm(durationH, durationM);

	if (start != "")
	{
		let date = to_stamp(start);

		/* Update this for both the table and the page. */
		$("#preview-start").html(date);
		$("#page-start").html(date);
	}

	/* Update the table preview. */
	$("#preview-length").html(lengthStr);
	$("#preview-location").html(locate);
	$("#preview-title").html(title);

	/* Update the page preview. */
	$("#page-title").html(title);
	$("#page-author").html(author);
	$("#page-location").html(locate);
	$("#page-duration").html(lengthStr);
	$("#page-points").html(points);
	$("#page-description").html(description);

	if (link != "")  $("#page-weblink").html("<a href='"+link+"' target='_blank'>External URL</a>");
	else             $("#page-weblink").empty();
}
function update_preview_loop()
{
	update_preview();
	setTimeout(update_preview_loop, 100);
}
