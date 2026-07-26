import copy


def deep_merge(original, changes):
    """
    Recursively merge dictionaries.
    """

    for key, value in changes.items():

        if (
            key in original
            and isinstance(original[key], dict)
            and isinstance(value, dict)
        ):

            deep_merge(
                original[key],
                value
            )

        else:

            original[key] = value

    return original


def apply_trip_changes(trip_plan, changes):

    updated_trip = copy.deepcopy(trip_plan)

    # ----------------------------
    # Handle day-by-day edits
    # ----------------------------

    if "days" in changes and isinstance(changes["days"], dict):

        for day_number, day_changes in changes["days"].items():

            try:

                index = int(day_number) - 1

            except ValueError:

                continue


            if 0 <= index < len(updated_trip["days"]):

                deep_merge(

                    updated_trip["days"][index],

                    day_changes

                )


        # Remove days so it isn't merged again
        del changes["days"]


    # ----------------------------
    # Merge everything else
    # ----------------------------

    deep_merge(
        updated_trip,
        changes
    )

    return updated_trip