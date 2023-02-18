/* Code edit submission. */
$("#edit-form").submit(function()
{
	if (!confirm("Are you sure you want to publish this edit?"))  return false;

	$.ajax({
		type: "POST",
		url: "/api/reward/edit/"+id,
		data: {"reward": $("#reward").val(), "value": $("#value").val(), "stock": $("#stock").val()},
		success: function()
		{
			location.href="/admin/rewards/manage";
		},
		error: function()
		{
			alert("Unexpected error occurred.");
		}
	});

	return false;
});
