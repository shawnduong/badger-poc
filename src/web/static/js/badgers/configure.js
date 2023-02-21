function preselect(stat, tending)
{
}

function load_options()
{
	$.getJSON("/api/badger/configurations", function (d)
	{
		$("#config-form").append("<input type='radio' name='option' value='0;0' id='0_0'>"+
			"<label for='0_0'>Idle</label><br>");
		$("#config-form").append("<input type='radio' name='option' value='2;0' id='2_0'>"+
			"<label for='2_0'>Rewards Station</label><br>");
		$("#config-form").append("<input type='radio' name='option' value='4;0' id='4_0'>"+
			"<label for='4_0'>Card Provisionment Station</label><br>");

		for (let i = 0; i < d.Events.length; i++)
		{
			$("#config-form").append("<input type='radio' name='option' value='1;"+d.Events[i].id+"' id='1_"+d.Events[i].id+"'>"+
				"<label for='1_"+d.Events[i].id+"'>Attendance Station for \""+d.Events[i].title+"\"</label><br>");
		}

		for (let i = 0; i < d.Stamps.length; i++)
		{
			$("#config-form").append("<input type='radio' name='option' value='3;"+d.Stamps[i].id+"' id='3_"+d.Stamps[i].id+"'>"+
				"<label for='3_"+d.Stamps[i].id+"'>Stamp Station for \""+d.Stamps[i].name+"\"</label><br>");
		}

		$("#config-form").append("<br><input type='submit' value='Submit'>");

		$(selected)[0].checked = true;
	});
}

$("#config-form").submit(function()
{
	if (!confirm("Are you sure you want to set this config?"))  return false;

	let option = $("input[name='option']:checked").map(function(_, e) { return $(e).val(); }).get()[0];

	$.ajax(
	{
		type: "POST",
		url: "/api/badger/configure/"+id,
		data: {"option": option},
		success: function()
		{
			location.href = "/admin/badgers/manage";
		},
		error: function()
		{
			alert("Unexpected error occurred.");
		}
	});

	return false;
});
