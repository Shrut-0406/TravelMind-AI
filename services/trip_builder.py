from services.map_service import (
    get_coordinates,
    extract_locations
)

from services.routing_service import (
    get_route_coordinates
)

from services.gas_service import (
    add_gas_stops
)

from services.weather_service import (
    get_weather_forecast
)

from services.image_service import (
    get_destination_image
)



def rebuild_trip_data(trip):


    # -------------------------
    # Destination image
    # -------------------------

    if not trip.image_url:

        trip.image_url = get_destination_image(
            trip.destination
        )



    # -------------------------
    # Build map locations
    # -------------------------

    map_locations = extract_locations(

        trip.trip_plan,

        trip.origin

    )



    # -------------------------
    # Add starting location
    # -------------------------

    origin_lat, origin_lon = get_coordinates(
        trip.origin
    )


    if origin_lat and origin_lon:

        map_locations.insert(

            0,

            {
                "day": 0,

                "time": "Start",

                "place": trip.origin,

                "activity": "Starting location",

                "lat": origin_lat,

                "lon": origin_lon

            }

        )



    # -------------------------
    # Road route
    # -------------------------

    route = get_route_coordinates(
        map_locations
    )


    # Fallback if OSRM fails

    if not route:

        route = [

            [
                location["lat"],
                location["lon"]
            ]

            for location in map_locations

        ]



    # -------------------------
    # Gas stations
    # -------------------------

    if trip.transportation.lower() in [

        "car",

        "rental car",

        "car rental",

        "drive"

    ]:


        gas_stops = add_gas_stops(
            route
        )


        if gas_stops:

            map_locations.extend(
                gas_stops
            )



    # -------------------------
    # Save map data
    # -------------------------

    trip.map_locations = map_locations

    trip.route_coordinates = route



    # -------------------------
    # Weather
    # -------------------------

    lat, lon = get_coordinates(
        trip.destination
    )


    if lat and lon:

        return get_weather_forecast(

            lat,

            lon

        )


    return []