/* Announcement edit submission. */
$("#edit-form").submit(function()
{
	if (!confirm("Are you sure you want to publish this edit?"))  return false;

	$.ajax(
	{
		type: "POST",
		url: "/api/announcement/edit/"+id,
		data: {"contents": $("#edit-content").val()},
		success: function()
		{
			location.href="/admin/announcements/manage";
		},
		error: function()
		{
			alert("Unexpected error occurred.");
		}
	});

	return false;
});

/* Announcement preview. */
function update_preview()
{
	let content = $("#edit-content").val();
	let t = to_stamp(e);
	$("#preview-content").html("<p><b>"+t+"</b> "+content+"</p>");
}
function update_preview_loop()
{
	update_preview();
	setTimeout(update_preview_loop, 100);
}

$(document).ready(function() { update_preview_loop(); });
