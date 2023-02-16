/* Load events. */
$(document).ready(function()
{
	$.getJSON("/api/event/list", function (data)
	{
		for (let i = data.Events.length-1; i >= 0; i--)
		{
			let t = new Date(data.Events[i].start * 1000);
			let dateStr = t.toLocaleDateString().slice(0, -5);
			let timeStr = t.toLocaleTimeString().slice(0, -6) + t.toLocaleTimeString().slice(-2);
			let stat = ""

			if (data.Events[i].status == 2)
				stat = "event-completed";
			else if (data.Events[i].status == 1)
				stat = "event-happening";
			else
				stat = "";

			$("#events-table-data").append(
				"<tr id='"+data.Events[i].id+"' class='"+stat+"'>" +
					"<td>"+dateStr+" "+timeStr+"</td>"+
					"<td>"+data.Events[i].length+"</td>"+
					"<td>"+data.Events[i].location+"</td>"+
					"<td class='event-title'>"+data.Events[i].title+"</td>"+
					"<td><center><h3><a class='nodecor' href='/events/"+data.Events[i].id+
						"'>&gt;&gt;</a></h3></center></td>"+
					"<td><center><span class='delete'></span> <span class='edit-icon'>"+
						"</span></center></td>"+
				"</tr>"
			);
		}
	});
});

/* Confirm before deleting an event. */
$(document).on("click", ".delete", function()
{
	id = $(this).parent().parent().parent()[0].id;
	text = $(this).parent().parent().parent().find(".event-title").text();
	if (!confirm("Are you sure you want to delete \""+text+"\"?"))  return;

	$.ajax({
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
	id = $(this).parent().parent().parent()[0].id;
	location.href="/admin/events/edit/"+id;
});
