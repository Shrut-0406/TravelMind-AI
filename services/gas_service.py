import requests
from math import radians, sin, cos, sqrt, atan2



# More reliable Overpass server
OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"





def calculate_distance(point1, point2):

    R = 6371

    lat1 = radians(point1[0])
    lon1 = radians(point1[1])

    lat2 = radians(point2[0])
    lon2 = radians(point2[1])


    dlat = lat2 - lat1
    dlon = lon2 - lon1


    a = (
        sin(dlat / 2) ** 2
        +
        cos(lat1)
        *
        cos(lat2)
        *
        sin(dlon / 2) ** 2
    )


    return R * 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )







def get_nearby_gas_station(lat, lon):


    query = f"""

    [out:json][timeout:25];

    node
    [
        amenity=fuel
    ]
    (around:15000,{lat},{lon});

    out 5;

    """



    try:


        response = requests.post(

            OVERPASS_URL,

            data=query,

            headers={
                "User-Agent": "TravelMindAI/1.0"
            },

            timeout=60

        )



        # Check server response

        if response.status_code != 200:

            print(
                "Overpass status:",
                response.status_code
            )

            print(
                response.text[:200]
            )

            return None




        # Convert JSON safely

        try:

            data = response.json()


        except Exception:


            print(
                "Invalid JSON from Overpass:"
            )


            print(
                response.text[:500]
            )


            return None





        stations = data.get(
            "elements",
            []
        )



        if not stations:

            return None





        # Pick first available station

        station = stations[0]



        tags = station.get(
            "tags",
            {}
        )



        return {

            "place":
                tags.get(
                    "name",
                    "Gas Station"
                ),


            "activity":
                "Fuel stop",


            "lat":
                station["lat"],


            "lon":
                station["lon"],


            "type":
                "gas"

        }





    except Exception as e:


        print(
            "Gas station error:",
            e
        )


        return None







def add_gas_stops(route_coordinates):


    gas_stops = []



    if len(route_coordinates) < 2:

        return gas_stops





    distance_total = 0


    next_stop_distance = 200



    previous_point = route_coordinates[0]





    for point in route_coordinates[1:]:



        distance_total += calculate_distance(

            previous_point,

            point

        )





        if distance_total >= next_stop_distance:



            station = get_nearby_gas_station(

                point[0],

                point[1]

            )



            if station:


                station.update({

                    "day": 0,

                    "time": "Fuel Stop"

                })


                gas_stops.append(

                    station

                )


                print(

                    "Added gas stop:",

                    station["place"]

                )



            next_stop_distance += 200





        previous_point = point





    return gas_stops