/* Convert epoch timestamp into a M/D HH:MM (PM/AM) string. */
function to_stamp(timestamp)
{
	let t = new Date(timestamp);
	let dateStr = t.toLocaleDateString().slice(0, -5);
	let timeStr = t.toLocaleTimeString().slice(0, -6) + t.toLocaleTimeString().slice(-2);

	return dateStr+" "+timeStr;
}
