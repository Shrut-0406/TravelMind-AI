import os
import requests


def get_destination_image(destination):

    api_key = os.getenv("PEXELS_API_KEY")


    url = "https://api.pexels.com/v1/search"


    headers = {
        "Authorization": api_key
    }


    params = {
        "query": f"{destination} travel",
        "per_page": 1
    }


    response = requests.get(
        url,
        headers=headers,
        params=params
    )


    if response.status_code == 200:

        data = response.json()


        if data["photos"]:

            return data["photos"][0]["src"]["large"]


    # fallback image
    return None