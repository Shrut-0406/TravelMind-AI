import requests


WEATHER_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",

    51: "Light Drizzle",
    53: "Drizzle",
    55: "Heavy Drizzle",

    61: "Light Rain",
    63: "Rain",
    65: "Heavy Rain",

    71: "Light Snow",
    73: "Snow",
    75: "Heavy Snow",

    80: "Rain Showers",
    81: "Rain Showers",
    82: "Heavy Rain Showers",

    95: "Thunderstorm",
    96: "Thunderstorm",
    99: "Severe Thunderstorm"
}


def get_weather_forecast(lat, lon):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&daily=weather_code,temperature_2m_max,"
        "temperature_2m_min,precipitation_probability_max"
        "&timezone=auto"
    )

    try:

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print("Weather API Error:", response.status_code)
            return []

        data = response.json()

        daily = data["daily"]

        forecast = []

        for i in range(len(daily["time"])):

            forecast.append({

                "date": daily["time"][i],

                "condition": WEATHER_CODES.get(
                    daily["weather_code"][i],
                    "Unknown"
                ),

                "high": daily["temperature_2m_max"][i],

                "low": daily["temperature_2m_min"][i],

                "rain": daily["precipitation_probability_max"][i]

            })

        return forecast

    except Exception as e:

        print("Weather Error:", e)

        return []