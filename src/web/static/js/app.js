let lastUpdatePoints = null;

/* Continuously update the page via AJAX. */
function refresh()
{
	$.getJSON("/api/user/info", function (data)
	{
		if (data.User.name == null) data.User.name = "Not set";
		if (data.User.email == null) data.User.email = "Not set";
		$("#name").text(data.User.name);
		$("#email").text(data.User.email);
	});
};
function refresh_loop()
{
	refresh();
	setTimeout(refresh_loop, 5000);
};

$(document).ready(function() { refresh_loop(); });

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
		data: {"name": $("#name-form").val()},
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
		data: {"email": $("#email-form").val()},
		success: function()
		{
			refresh();
			$("#email-container").attr("hidden", false);
			$("#email-edit-container").attr("hidden", true);
		}
	});

	return false;
});
