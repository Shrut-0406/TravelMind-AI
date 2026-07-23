import requests


def get_route_coordinates(locations):

    """
    Gets real road route coordinates from OSRM.

    Input:
    [
        {"lat":50.44,"lon":-104.61},
        {"lat":51.17,"lon":-115.57}
    ]

    Returns:
    [
        [lat, lon],
        [lat, lon],
        ...
    ]
    """

    if len(locations) < 2:
        return []


    coordinates = ";".join(
        [
            f"{location['lon']},{location['lat']}"
            for location in locations
        ]
    )


    url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{coordinates}"
    )


    params = {

        "overview": "full",

        "geometries": "geojson"

    }


    try:

        response = requests.get(

            url,

            params=params,

            timeout=15

        )


        data = response.json()


        if data["code"] != "Ok":

            return []


        route = data["routes"][0]


        coordinates = route["geometry"]["coordinates"]


        # OSRM returns:
        # longitude, latitude

        return [

            [
                point[1],
                point[0]
            ]

            for point in coordinates

        ]


    except Exception as e:

        print("Routing error:", e)

        return []