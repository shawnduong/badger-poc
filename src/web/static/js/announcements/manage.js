/* Confirm before deleting an announcement. */
$(document).on("click", ".delete", function()
{
	let tr = $(this).parent().parent().parent();
	let id = tr[0].id;
	let content = tr.find(".announcement-contents").text();
	let text = "";

	if (content.length > 24)
		text = content.slice(0, 24)+"...";
	else
		text = content;

	if (!confirm("Are you sure you want to delete \""+text+"\"?"))  return;

	$.ajax(
	{
		type: "POST",
		url: "/api/announcement/delete/"+id,
		success: function()
		{
			location.href="/admin/announcements/manage";
		},
		error: function()
		{
			alert("Unexpected error occurred.");
		}
	});
});

/* Edit an announcement. */
$(document).on("click", ".edit-icon", function()
{
	let tr = $(this).parent().parent().parent();
	let id = tr[0].id;
	location.href="/admin/announcements/edit/"+id;
});
