"""Simple weather fetcher with a sample-data fallback.

Provides `fetch_current_weather(api_key, city)` which returns a dict with
`city`, `temp_c`, `description`, and `raw` fields. If `api_key` is falsy,
deterministic sample data is returned so the app can be used offline for testing.
"""
from typing import Dict, Any, Optional

SAMPLE = {
    "city": "Sampleville",
    "temp_c": 21.5,
    "description": "clear sky",
    "raw": {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 21.5},
        "name": "Sampleville",
    },
}


def fetch_current_weather(api_key: str, city: str = "London") -> Dict[str, Any]:
    """Legacy helper kept for tests: returns sample when no api_key.

    This function is preserved for backward compatibility and testing.
    For the GUI and location lookup use `fetch_weather_for_location`.
    """
    if not api_key:
        return SAMPLE.copy()

    try:
        import requests
    except Exception as e:
        raise RuntimeError("The 'requests' package is required to fetch live data") from e

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    return {
        "city": data.get("name"),
        "temp_c": data.get("main", {}).get("temp"),
        "description": (data.get("weather") or [{}])[0].get("description"),
        "raw": data,
    }


def geocode_location(query: str) -> Optional[Dict[str, Any]]:
    """Geocode a free-text location (city, state or ZIP) using Nominatim.

    Returns a dict with `lat`, `lon`, and `display_name`, or None if not found.
    """
    if not query:
        return None

    try:
        import requests
    except Exception as e:
        raise RuntimeError("The 'requests' package is required for geocoding") from e

    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json", "limit": 1}
    headers = {"User-Agent": "weather_app/1.0 (+https://example.com)"}
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        return None

    item = data[0]
    return {"lat": float(item["lat"]), "lon": float(item["lon"]), "display_name": item.get("display_name")}


def fetch_weather_for_location(location: str) -> Dict[str, Any]:
    """Geocode `location` and fetch weather from Open-Meteo using coordinates.

    Uses Open-Meteo API with `hourly=temperature_2m` and `current_weather=true`.
    Returns a dict with `city`, `lat`, `lon`, `temp_c`, and `raw`.
    """
    geo = geocode_location(location)
    if not geo:
        raise ValueError(f"Could not geocode location: {location}")

    lat = geo["lat"]
    lon = geo["lon"]

    try:
        import requests
    except Exception as e:
        raise RuntimeError("The 'requests' package is required to fetch weather") from e

    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "hourly": "temperature_2m", "current_weather": "true", "timezone": "auto"}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    # Prefer current_weather if available
    temp = None
    if "current_weather" in data and data["current_weather"]:
        temp = data["current_weather"].get("temperature")

    return {"city": geo.get("display_name"), "lat": lat, "lon": lon, "temp_c": temp, "raw": data}

