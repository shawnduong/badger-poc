$(document).ready(function()
{
	console.log(e);
	let t = new Date(e);
	$("#timestamp").text(t.toLocaleDateString()+" "+t.toLocaleTimeString());
});


/* Announcement edit submission. */
$("#announcement-edit-form").submit(function()
{
	if (!confirm("Are you sure you want to publish this edit?"))  return;

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
