/* Announcement edit submission. */
$("#announcement-edit-form").submit(function()
{
	if (!confirm("Are you sure you want to publish this edit?"))  return false;

	$.ajax({
		type: "POST",
		url: "/api/announcement/edit/"+id,
		data: {"contents": $("#announcement-edit-content").val()},
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
	let content = $("#announcement-edit-content").val();
	let t = new Date(Date.now());
	let time = t.toLocaleDateString().slice(0, -5)+" "+
		t.toLocaleTimeString().slice(0, -6)+t.toLocaleTimeString().slice(-2);
	$("#announcement-edit-preview-content").html("<p><b>"+time+"</b> "+content+"</p>");
}
function update_preview_loop()
{
	update_preview();
	setTimeout(update_preview_loop, 100);
}

$(document).ready(function()
{
	console.log(e);
	let t = new Date(e);
	$("#timestamp").text(t.toLocaleDateString()+" "+t.toLocaleTimeString());
	update_preview_loop();
});

