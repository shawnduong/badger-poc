/* Convert epoch timestamp into a M/D HH:MM (PM/AM) string. */
function to_stamp(timestamp)
{
	let t = new Date(timestamp);
	let dateStr = t.toLocaleDateString().slice(0, -5);
	let timeStr = t.toLocaleTimeString().slice(0, -6) + t.toLocaleTimeString().slice(-2);

	return dateStr+" "+timeStr;
}

/* Convert epoch timestamp into a M/D HH:MM:SS (PM/AM) string. */
function to_full_stamp(timestamp)
{
	let t = new Date(timestamp);
	let dateStr = t.toLocaleDateString();
	let timeStr = t.toLocaleTimeString();

	return dateStr+" "+timeStr;
}

/* Convert h and m into an HhMm string. */
function to_HhMm(H, M)
{
	let str = "";
	if (H > 0) str += H+"h";
	if (M > 0) str += M+"m";

	return str;
}
