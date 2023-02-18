/* Code edit submission. */
$("#edit-form").submit(function()
{
	if (!confirm("Are you sure you want to publish this edit?"))  return false;

	$.ajax({
		type: "POST",
		url: "/api/code/edit/"+id,
		data: {"code": $("#code").val(), "value": $("#value").val(), "note": $("#note").val()},
		success: function()
		{
			location.href="/admin/codes/manage";
		},
		error: function()
		{
			alert("Unexpected error occurred.");
		}
	});

	return false;
});
