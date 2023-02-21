/* Stamp edut submission. */
$("#edit-form").submit(function()
{
	if (!confirm("Are you sure you want to publish this edit?"))  return false;

	$.ajax({
		type: "POST",
		url: "/api/stamp/edit/"+id,
		data: {"name": $("#stamp").val(), "slots": $("#slots").val(), "cooldown": $("#cooldown").val()},
		success: function()
		{
			location.href="/admin/stamps/manage";
		},
		error: function()
		{
			alert("Unexpected error occurred.");
		}
	});

	return false;
});
