def to_hm(epoch: int) -> str:
	"""
	Convert an epoch timestamp (seconds) to an {hours}h{minutes}m string.
	"""

	string = ""

	if (n:=(epoch // 3600)) > 0:
		string += f"{n}h"
	if (n:=((epoch % 3600) // 60)) > 0:
		string += f"{n}m"

	return string

