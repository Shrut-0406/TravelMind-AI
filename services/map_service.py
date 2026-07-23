import requests
import time



def get_coordinates(place, context=None):

    """
    Returns latitude and longitude for a place.
    """

    url = "https://nominatim.openstreetmap.org/search"


    if context:

        query = f"{place}, {context}"

    else:

        query = place


    params = {

        "q": query,

        "format": "json",

        "limit": 5,

    }


    headers = {

        "User-Agent": "TravelMindAI/1.0"

    }


    try:

        response = requests.get(

            url,

            params=params,

            headers=headers,

            timeout=10

        )


        # Debug status

        if response.status_code != 200:

            print(
                "Nominatim error:",
                response.status_code
            )

            return None, None



        data = response.json()



        if not data:

            print(
                "Location not found:",
                place
            )

            return None, None



        return (

            float(data[0]["lat"]),

            float(data[0]["lon"])

        )



    except Exception as e:

        print(
            "Map error:",
            place,
            e
        )

        return None, None





def extract_locations(trip_plan, origin):

    locations = []

    seen_places = set()


    # Add starting location first

    lat, lon = get_coordinates(origin)

    if lat and lon:

        locations.append({
            "day": 0,
            "time": "Start",
            "place": origin,
            "activity": "Starting location",
            "lat": lat,
            "lon": lon
        })

        seen_places.add(origin.lower())



    for day_number, day in enumerate(
        trip_plan["days"],
        start=1
    ):

        activities = [
            ("Morning", day["morning"]),
            ("Afternoon", day["afternoon"]),
            ("Evening", day["evening"])
        ]


        for time_of_day, activity in activities:

            place = activity["place"]


            if place.lower() in seen_places:
                continue


            lat, lon = get_coordinates(place)


            if lat and lon:

                locations.append({
                    "day": day_number,
                    "time": time_of_day,
                    "place": place,
                    "activity": activity["activity"],
                    "lat": lat,
                    "lon": lon
                })


                seen_places.add(place.lower())


    return locations

    MAX_LOCATIONS = 10


    locations = []



    seen_places = set()



    for day_number, day in enumerate(

        trip_plan["days"],

        start=1

    ):



        activities = [

            ("Morning", day["morning"]),

            ("Afternoon", day["afternoon"]),

            ("Evening", day["evening"])

        ]



        for time_of_day, activity in activities:



            place = activity["place"]



            # Avoid duplicate searches

            if place in seen_places:

                continue


            seen_places.add(place)



            lat, lon = get_coordinates(

                place,

                destination

            )



            if lat and lon:


                locations.append({

                    "day": day_number,

                    "time": time_of_day,

                    "place": place,

                    "activity": activity["activity"],

                    "lat": lat,

                    "lon": lon

                })



            # Respect API limits

            time.sleep(3)



    return locations[:MAX_LOCATIONS]