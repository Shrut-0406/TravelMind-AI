import os
import requests

from dotenv import load_dotenv


load_dotenv()


GEOAPIFY_API_KEY = os.getenv(
    "GEOAPIFY_API_KEY"
)


CATEGORY_MAP = {

    "Hotel":
        "accommodation.hotel",

    "Hostel":
        "accommodation.hostel",
    
    "Airbnb":
        "accommodation.guest_house",

    "Camping":
        "accommodation.campsite",


    "Motel":
        "accommodation.motel",

    "Guest House":
        "accommodation.guest_house",

    "Resort":
        "accommodation.resort",

    "Vacation Rental":
        "accommodation.guest_house",

}


def get_nearby_accommodations(
    lat,
    lon,
    accommodation_type,
    radius=5000
):
    """
    Find nearby accommodations using Geoapify.

    Inputs:
        lat                 -> destination latitude
        lon                 -> destination longitude
        accommodation_type  -> Hotel, Hostel, Motel, etc.
        radius              -> search radius in meters

    Returns:
        [
            {
                "type",
                "name",
                "address",
                "lat",
                "lon",
                "phone",
                "website"
            }
        ]
    """

    if not GEOAPIFY_API_KEY:

        print(
            "Missing GEOAPIFY_API_KEY"
        )

        return []


    category = CATEGORY_MAP.get(

        accommodation_type,

        "accommodation.hotel"

    )


    url = "https://api.geoapify.com/v2/places"


    params = {

        "categories": category,

        # Geoapify expects longitude first
        "filter":
            f"circle:{lon},{lat},{radius}",

        "limit":
            20,

        "apiKey":
            GEOAPIFY_API_KEY

    }


    try:

        response = requests.get(

            url,

            params=params,

            timeout=20

        )


        if response.status_code != 200:

            print(
                "Geoapify error:",
                response.text
            )

            return []


        data = response.json()


        features = data.get(
            "features",
            []
        )


        accommodations = []


        bad_names = {

            "lobby",

            "parking",

            "parkade"

        }


        for item in features:

            properties = item.get(
                "properties",
                {}
            )


            name = properties.get(
                "name"
            )


            if not name:
                continue


            if name.lower() in bad_names:
                continue


            accommodation = {

                "type":
                    accommodation_type,

                "name":
                    name,

                "address":
                    properties.get(
                        "formatted",
                        "Address unavailable"
                    ),

                "lat":
                    properties.get(
                        "lat"
                    ),

                "lon":
                    properties.get(
                        "lon"
                    ),

                "phone":
                    properties.get(
                        "phone"
                    ),

                "website":
                    properties.get(
                        "website"
                    )

            }


            accommodations.append(
                accommodation
            )


        return accommodations


    except Exception as e:

        print(
            "Accommodation API error:",
            e
        )

        return []