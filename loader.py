'''
Script to load geographical data into a pandas DataFrame, and save it as a CSV file.
'''

from geopy.exc import GeopyError
from geopy.geocoders import Nominatim
import numpy as np
import pandas as pd


def get_geolocator(agent='h501-student'):
    """
    Initiate a Nominatim geolocator instance given an `agent`.

    Parameters
    ----------
    agent : str, optional
        Agent name for Nominatim, by default 'h501-student'
    """
    return Nominatim(user_agent=agent)


def fetch_location_data(geolocator, loc):
    """
    Geocode a single location string.

    Parameters
    ----------
    geolocator : geopy.geocoders.Nominatim
        Geolocator instance used to look up the location.
    loc : str
        Name of the location to look up.

    Returns
    -------
    dict
        Location name, latitude, longitude, and type. If the location
        cannot be found (or the lookup fails), everything except the
        location name is NaN.
    """
    try:
        location = geolocator.geocode(loc)
    except GeopyError as e:
        print(f"Lookup failed for {loc!r}: {e}")
        location = None

    if location is None:
        return {"location": loc, "latitude": np.nan,
                "longitude": np.nan, "type": np.nan}

    loc_type = location.raw.get("type")

    return {"location": loc,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "type": loc_type.title() if loc_type else np.nan}


def build_geo_dataframe(geolocator, locations):
    """
    Build a DataFrame of geocoded locations.

    Parameters
    ----------
    geolocator : geopy.geocoders.Nominatim
        Geolocator instance used to look up each location.
    locations : list of str
        Location names to look up.

    Returns
    -------
    pandas.DataFrame
        One row per location with columns location, latitude,
        longitude, and type.
    """
    geo_data = [fetch_location_data(geolocator, loc) for loc in locations]

    return pd.DataFrame(geo_data)


if __name__ == "__main__":
    geo = get_geolocator()

    locations = ["Museum of Modern Art", "iuyt8765(*&)", "Alaska",
                 "Franklin's Barbecue", "Burj Khalifa"]

    df = build_geo_dataframe(geo, locations)

    df.to_csv("./geo_data.csv", index=False)
