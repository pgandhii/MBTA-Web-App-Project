import os
import json
import urllib.request 
import urllib.parse

from dotenv import load_dotenv

# Load environment variables
load_dotenv("secret.env")

# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


# Helpful error messages if keys are missing
if MAPBOX_TOKEN is None:
    raise RuntimeError("MAPBOX_TOKEN is not set. Check your .env file.")
if MBTA_API_KEY is None:
    raise RuntimeError("MBTA_API_KEY is not set. Check your .env file.")

# Useful base URLs (you need to add the appropriate parameters for each API request)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
MBTA_BASE_URL = "https://api-v3.mbta.com/"


# A little bit of scaffolding if you want to use it
def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_lng() and get_nearest_station() might need to use this function.
    """
    with urllib.request.urlopen(url) as response:
        data = response.read().decode("utf-8")
        return json.loads(data)


def get_lat_lng(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/search-box/#search-request for Mapbox Search API URL formatting requirements.
    """
    place_encoded = urllib.parse.quote(place_name)

    url = (
        f"https://api.mapbox.com/geocoding/v5/mapbox.places/"
        f"{place_encoded}.json?access_token={MAPBOX_TOKEN}&limit=1"
    )

    data = get_json(url)
    print("MAPBOX RAW RESPONSE:", json.dumps(data, indent=2))

    features = data.get("features", [])
    if not features:
        return None, None
    
    lng, lat = features[0]["geometry"]["coordinates"]
    return str(lat), str(lng)

def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool, str]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible, system_type)
    tuple for the nearest MBTA station to the given coordinates.
    """
    params = {
        "api_key": MBTA_API_KEY,
        "sort": "distance",
        "filter[latitude]": latitude,
        "filter[longitude]": longitude,
        "page[limit]": 1,
    }

    url = f"{MBTA_BASE_URL}stops?{urllib.parse.urlencode(params)}"
    print("DEBUG MBTA URL:", url)
    data = get_json(url)
    print("DEBUG MBTA RESPONSE:", json.dumps(data, indent=2))

    stops = data.get("data", [])
    if not stops:
        return None, None, "Unknown"

    first_stop = stops[0]
    attrs = first_stop.get("attributes", {})

    system_type = "MBTA Transit"

    name = attrs.get("name")
    wheelchair_boarding = attrs.get("wheelchair_boarding", 0)

    # MBTA codes: 1 = accessible, 2 = not accessible, 0 = no info
    wheelchair_accessible = wheelchair_boarding == 1

    return name, wheelchair_accessible, system_type


def get_nearest_station_with_type(latitude: str, longitude: str, route_type: str):
    """
    Same as get_nearest_station but allows filtering by MBTA route_type.
    route_type options:
        "all" → no filter
        "0"   → Light Rail (Green Line)
        "1"   → Subway
        "2"   → Commuter Rail
        "3"   → Bus
        "4"   → Ferry
    """
    params = {
        "api_key": MBTA_API_KEY,
        "sort": "distance",
        "filter[latitude]": latitude,
        "filter[longitude]": longitude,
        "page[limit]": 1,
    }

    if route_type != "all":
        params["filter[route_type]"] = route_type

    url = f"{MBTA_BASE_URL}stops?{urllib.parse.urlencode(params)}"
    data = get_json(url)

    stops = data.get("data", [])
    if not stops:
        return None

    attrs = stops[0]["attributes"]
    name = attrs.get("name")
    wheelchair = attrs.get("wheelchair_boarding", 0) == 1

    # station coordinates (needed for weather)
    lat = float(attrs.get("latitude"))
    lng = float(attrs.get("longitude"))

    return {
        "name": name,
        "wheelchair_accessible": wheelchair,
        "lat": lat,
        "lng": lng,
    }

# Weather API key
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(lat: float, lng: float):
    """
    Returns weather info near the station.
    """
    if OPENWEATHER_API_KEY is None:
        return None

    params = {
        "lat": lat,
        "lon": lng,
        "appid": OPENWEATHER_API_KEY,
        "units": "imperial"
    }

    url = "https://api.openweathermap.org/data/2.5/weather?" + urllib.parse.urlencode(params)
    data = get_json(url)

    try:
        return {
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "city": data.get("name", "")
        }
    except:
        return None

def find_stop_near_with_weather(place_name: str):
    """
    Returns nearest MBTA station + accessibility + weather.
    Used by the Flask app.
    """
    # Step 1: get coordinates for the place
    lat, lng = get_lat_lng(place_name)
    if lat is None or lng is None:
        return None

    # Step 2: get nearest station using the SAME logic that already works
    stop_name, wheelchair_accessible, system_type = get_nearest_station(lat, lng)
    if stop_name is None:
        return None

    # Step 3: get weather near that location
    weather = get_weather(float(lat), float(lng))

    # Step 4: return a dict that app.py expects
    return {
        "stop": stop_name,
        "wheelchair_accessible": wheelchair_accessible,
        "weather": weather,
        "system_type": system_type
    }



def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    lat, lng = get_lat_lng(place_name)
    if lat is None or lng is None:
        return None, None

    return get_nearest_station(lat, lng)


def main():
    """
    You should test all the above functions here
    """
    test_place = "Boston Common"
    print("Testing with:", test_place)
    print("Coordinates:", get_lat_lng(test_place))
    print("Nearest stop + accessible:", find_stop_near(test_place))


if __name__ == "__main__":
    main()