"""Helper utilities for cleaning SimaPro exports."""

import re
from typing import Any

from .config import KNOWN_AREA_STRINGS, LOCATION_CODES

_SUBDIVISION_PATTERN = re.compile(
	r"^(%s)-[A-Z0-9]+$" % '|'.join(sorted(re.escape(code) for code in LOCATION_CODES))
)


def strip_country_code(value: Any) -> str:
	"""Remove trailing region/country hints like "{US}" or ", US"."""
	val = str(value).strip()
	val = re.sub(
		r"\{([^{}]+)\}",
		lambda match: '' if match.group(1).strip() in LOCATION_CODES or match.group(1).strip() in KNOWN_AREA_STRINGS else match.group(0),
		val,
	)
	val = re.sub(r",\s*,", ',', val)
	val = val.strip().strip(',')

	tail_match = re.match(r"(.+),\s*([^,]+)$", val)
	if not tail_match:
		return val

	main, tail = tail_match.group(1).strip(), tail_match.group(2).strip()
	if tail in LOCATION_CODES:
		return main
	if _SUBDIVISION_PATTERN.match(tail):
		return main
	if tail in KNOWN_AREA_STRINGS:
		return main
	if tail.startswith('Europe without') or tail.startswith('North America without') or tail.startswith('Canada without'):
		return main
	return val


def is_number(value: Any) -> bool:
	"""Return True if the provided value looks like a numeric token."""
	try:
		return re.fullmatch(r"[\d,.]+", str(value).replace(' ', '')) is not None
	except TypeError:
		return False
