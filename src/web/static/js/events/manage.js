/* Confirm before deleting an event. */
$(document).on("click", ".delete", function()
{
	let tr = $(this).parent().parent().parent();
	let id = tr[0].id;
	let text = tr.find(".event-title").text();

	if (!confirm("Are you sure you want to delete \""+text+"\"?"))  return;

	$.ajax(
	{
		type: "POST",
		url: "/api/event/delete/"+id,
		success: function()
		{
			location.href="/admin/events/manage";
		},
		error: function()
		{
			alert("Unexpected error occurred.");
		}
	});
});

/* Edit an event. */
$(document).on("click", ".edit-icon", function()
{
	let tr = $(this).parent().parent().parent();
	let id = tr[0].id;
	location.href="/admin/events/edit/"+id;
});
