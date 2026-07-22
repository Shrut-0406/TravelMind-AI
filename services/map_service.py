import requests
import time



def get_coordinates(place):

    """
    Returns latitude and longitude for a place.
    """

    url = "https://nominatim.openstreetmap.org/search"


    params = {

        "q": place + ", Canada",

        "format": "json",

        "limit": 1

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





def extract_locations(trip_plan):

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

        ]



        for time_of_day, activity in activities:



            place = activity["place"]



            # Avoid duplicate searches

            if place in seen_places:

                continue


            seen_places.add(place)



            lat, lon = get_coordinates(

                place

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