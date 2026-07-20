def analyze_budget(
    budget,
    adults,
    children,
    days,
    transportation,
    accommodation
):

    travelers = adults + children

    # destination_multiplier = 1
    

    # if destination.lower() in [
    #     "banff",
    #     "vancouver",
    #     "toronto",
    #     "new york"
    # ]:

    #     destination_multiplier = 1.3


    # Basic estimates
    estimates = {
        "food": travelers * days * 40,
        "activities": travelers * days * 25,
    }


    # Accommodation estimate
    if accommodation.lower() == "hotel":
        estimates["accommodation"] = days * 220

    elif accommodation.lower() == "airbnb":
        estimates["accommodation"] = days * 100

    else:
        estimates["accommodation"] = days * 50



    # Transportation estimate
    if transportation.lower() == "car":
        estimates["transportation"] = days * 40

    elif transportation.lower() == "flight":
        estimates["transportation"] = travelers * 300

    else:
        estimates["transportation"] = days * 20



    estimated_total = sum(
        estimates.values()
    )


    if budget >= estimated_total:

        status = "Good"

        message = (
            "Your budget is realistic "
            "for this trip."
        )

    elif budget >= estimated_total * 0.8:

        status = "Tight"

        message = (
            "Your budget is possible, "
            "but some cheaper options "
            "may be needed."
        )

    else:

        status = "Low"

        message = (
            "Your budget may be too low "
            "for this trip."
        )


    return {

        "status": status,

        "message": message,

        "estimated_cost": estimates,

        "estimated_total": estimated_total,

        "per_person": round(
            budget / travelers,
            2
        )

    }