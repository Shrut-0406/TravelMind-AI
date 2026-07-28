import re


def find_overnight_locations(trip_plan, destination):
    """
    Returns a list of overnight locations.

    Example:
    [
        {
            "day": 1,
            "city": "Calgary"
        },
        {
            "day": 2,
            "city": "Banff"
        }
    ]
    """

    overnight_locations = []

    days = trip_plan.get("days", [])

    for day in days:

        city = None

        # Look through every activity
        for period in [
            "morning",
            "afternoon",
            "evening"
        ]:

            section = day.get(period, {})

            text = ""

            if isinstance(section, dict):
                text = section.get("activity", "")

            elif isinstance(section, str):
                text = section

            lower = text.lower()

            if (
                "check in" in lower
                or "hotel" in lower
                or "stay in" in lower
                or "overnight" in lower
            ):

                match = re.search(
                    r"in ([A-Za-z\s]+)",
                    text
                )

                if match:
                    city = match.group(1).strip()

        # If no overnight city found,
        # assume destination for final day
        if city is None and day.get("day") == len(days):
            city = destination

        if city:

            overnight_locations.append({

                "day": day["day"],

                "city": city

            })

    return overnight_locations