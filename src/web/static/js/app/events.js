let ahidden = true;
let ehidden = true;
let bhidden = true;

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
	$.ajax(
	{
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
	$.ajax(
	{
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
	$.ajax(
	{
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

/* Un/hide announcements. */
$("#announcements-expand-toggle").click(function()
{
	if (ahidden)
	{
		ahidden = false;
		$(".aextra").each(function () { $(this).attr("hidden", false) });
		$("#announcements-expand-toggle").text("Collapse");
	}
	else
	{
		ahidden = true;
		$(".aextra").each(function () { $(this).attr("hidden", true) });
		$("#announcements-expand-toggle").text("Expand");
	}
});

/* Un/hide events. */
$("#events-expand-toggle").click(function()
{
	if (ehidden)
	{
		ehidden = false;
		$(".eextra").each(function () { $(this).attr("hidden", false) });
		$("#events-expand-toggle").text("Collapse");
	}
	else
	{
		ehidden = true;
		$(".eextra").each(function () { $(this).attr("hidden", true) });
		$("#events-expand-toggle").text("Expand");
	}
});

/* Un/hide points breakdown. */
$("#badge-expand-toggle").click(function()
{
	if (bhidden)
	{
		bhidden = false;
		$("#badge-breakdown-container").attr("hidden", false);
		$("#badge-expand-toggle").text("Collapse");
	}
	else
	{
		bhidden = true;
		$("#badge-breakdown-container").attr("hidden", true);
		$("#badge-expand-toggle").text("Points Breakdown");
	}
});

/* Reward confirmation. */
$(document).on("click", ".claim", function()
{
	let tr = $(this).parent();
	let id = tr[0].id;
	let prize = tr.find(".reward-contents").text();
	let value = tr.find(".reward-value").text();

	if (!confirm("Are you sure you want to redeem "+prize+" for "+value+" points?"))  return;

	$.ajax(
	{
		type: "POST",
		url: "/api/reward/redeem/"+id,
		data: {"name": $("#entry-name").val()},
		success: function()
		{
			refresh();
		},
		error: function()
		{
			alert("Claim failed. Out of stock, already claimed, or insufficient points.");
		}
	});

	return false;
});
