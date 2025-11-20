import os
import json
import urllib.request

from dotenv import load_dotenv

# Load environment variables
load_dotenv("secret.env")

# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

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

    #Nidhi, I changed this code because it was throwing an error with flask
    # params = {
    #     "access_token": MAPBOX_TOKEN,
    #     "q": place_name,
    #     "limit": 1,
    # }

    # url = f"{MAPBOX_BASE_URL}?{urllib.parse.urlencode(params)}"
    # data = get_json(url)

    # features = data.get("features", [])
    # if not features:
    #     # No results found
    #     return None, None

    # # Mapbox returns coordinates as [longitude, latitude]
    # coords = features[0]["geometry"]["coordinates"]
    # lng, lat = coords

    # # Return as strings (matches type hint tuple[str, str])
    # return str(lat), str(lng)


def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates. wheelchair_accessible is True if the stop is marked as accessible, False otherwise.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    params = {
        "api_key": MBTA_API_KEY,
        "sort": "distance",
        "filter[latitude]": latitude,
        "filter[longitude]": longitude,
        "page[limit]": 1,
    }

    url = f"{MBTA_BASE_URL}stops?{urllib.parse.urlencode(params)}"
    data = get_json(url)

    stops = data.get("data", [])
    if not stops:
        return None, None

    first_stop = stops[0]
    attrs = first_stop.get("attributes", {})

    name = attrs.get("name")
    wheelchair_boarding = attrs.get("wheelchair_boarding", 0)

    # MBTA codes: 1 = accessible, 2 = not accessible, 0 = no info
    wheelchair_accessible = wheelchair_boarding == 1

    return name, wheelchair_accessible


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
    test_place = "Wellesley"
    print("Testing with:", test_place)
    print("Coordinates:", get_lat_lng(test_place))
    print("Nearest stop + accessible:", find_stop_near(test_place))


if __name__ == "__main__":
    main()