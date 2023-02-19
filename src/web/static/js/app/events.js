/* Name change dialogue. */
$("#edit-name").click(function()
{
	$("#name-container").attr("hidden", true);
	$("#name-edit-container").attr("hidden", false);
});
$("#name-edit-cancel").click(function()
{
	$("#name-container").attr("hidden", false);
	$("#name-edit-container").attr("hidden", true);
});
$("#name-edit-form").submit(function()
{
	$.ajax({
		type: "POST",
		url: "/api/user/edit/name",
		data: {"name": $("#entry-name").val()},
		success: function()
		{
			refresh();
			$("#name-container").attr("hidden", false);
			$("#name-edit-container").attr("hidden", true);
		}
	});

	return false;
});

/* Email change dialogue. */
$("#edit-email").click(function()
{
	$("#email-container").attr("hidden", true);
	$("#email-edit-container").attr("hidden", false);
});
$("#email-edit-cancel").click(function()
{
	$("#email-container").attr("hidden", false);
	$("#email-edit-container").attr("hidden", true);
});
$("#email-edit-form").submit(function()
{
	$.ajax({
		type: "POST",
		url: "/api/user/edit/email",
		data: {"email": $("#entry-email").val()},
		success: function()
		{
			refresh();
			$("#email-container").attr("hidden", false);
			$("#email-edit-container").attr("hidden", true);
		}
	});

	return false;
});

/* Code submission dialogue. */
$("#code-submit-form").submit(function()
{
	$.ajax({
		type: "POST",
		url: "/api/code/submit/"+$("#entry-code").val(),
		success: function()
		{
			$("#entry-code").val("");
			refresh();
		},
		error: function()
		{
			alert("Invalid code or already redeemed.");
		}
	});

	return false;
});
