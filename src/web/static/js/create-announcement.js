/* Announcement submission. */
$("#announcement-creation-form").submit(function()
{
	if (!confirm("Are you sure you want to publish this announcement?"))  return;

	$.ajax({
		type: "POST",
		url: "/api/announcement/create",
		data: {"timestamp": Date.now(), "content": $("#announcement-creation-content").val()},
		success: function()
		{
			location.href="/admin/announcements/manage"
		},
		error: function()
		{
			alert("Unexpected error occurred.");
		}
	});

	return false;
});

/* Announcement preview. */
$("#announcement-creation-preview-button").click(function()
{
	alert("Not implemented yet.");
});
