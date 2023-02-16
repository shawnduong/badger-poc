/* Event preview. */
function update_preview()
{
	let title = $("#event-title").val();
	let author = $("#event-author").val();
	let locate = $("#event-location").val();
	let start = $("#event-start").val();
	let durationH = $("#event-duration-hours").val();
	let durationM = $("#event-duration-minutes").val();
	let points = $("#event-points").val();
	let link = $("#event-weblink").val();
	let description = $("#event-description").val();

	let lengthStr = "";
	if (durationH > 0) { lengthStr += durationH +"h"};
	if (durationM > 0) { lengthStr += durationM +"m"};


	if (start != "")
	{
		let d = new Date(start);
		let date = d.toLocaleDateString().slice(0, -5)+" "+
			d.toLocaleTimeString().slice(0, -6)+d.toLocaleTimeString().slice(-2);

		/* Update this for both the table and the page. */
		$("#event-preview-start").html(date);
		$("#event-page-start").html(date);
	}

	/* Update the table preview. */
	$("#event-preview-length").html(lengthStr);
	$("#event-preview-location").html(locate);
	$("#event-preview-title").html(title);

	/* Update the page preview. */
	$("#event-page-title").html(title);
	$("#event-page-author").html(author);
	$("#event-page-room").html(locate);
	$("#event-page-duration").html(lengthStr);
	$("#event-page-points").html(points);
	$("#event-page-description").html(description);

	if (link != "")  $("#event-page-weblink").html("<a href='"+link+"' target='_blank'>External URL</a>");
	else             $("#event-page-weblink").empty();
}
function update_preview_loop()
{
	update_preview();
	setTimeout(update_preview_loop, 100);
}

$(document).ready(function() { update_preview_loop(); });
