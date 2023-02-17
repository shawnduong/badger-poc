/* Announcement submission. */
$("#announcement-creation-form").submit(function()
{
	if (!confirm("Are you sure you want to publish this announcement?"))  return false;

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
function update_preview()
{
	let content = $("#announcement-creation-content").val();
	let t = new Date(Date.now());
	let time = t.toLocaleDateString().slice(0, -5)+" "+
		t.toLocaleTimeString().slice(0, -6)+t.toLocaleTimeString().slice(-2);
	$("#announcement-creation-preview-content").html("<p><b>"+time+"</b> "+content+"</p>");
}
function update_preview_loop()
{
	update_preview();
	setTimeout(update_preview_loop, 100);
}

$(document).ready(function() { update_preview_loop(); });
