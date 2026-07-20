import requests


def get_coordinates(destination):
    """
    Returns (latitude, longitude) for a destination.
    Returns (None, None) if not found.
    """

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": destination,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "TravelMindAI"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        data = response.json()

        if not data:
            return None, None

        latitude = float(data[0]["lat"])
        longitude = float(data[0]["lon"])

        return latitude, longitude

    except Exception:
        return None, None