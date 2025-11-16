"""api.py

Provide function(s) to interact with the OMDB API.

This module allows fetching movie information by title using the
OMDB API. The API key is retrieved from the project's configuration.
Returned data includes the movie's title, director, release year,
and poster URL if available.
"""
import requests
from config import OMDB_API_KEY

OMDB_API_URL = "https://www.omdbapi.com/"


def fetch_omdb_by_title(title):
    """Fetch movie details from OMDB by movie title.

    Args:
        title (str): The title of the movie to search for.

    Returns:
        dict: A dictionary containing the following keys:
            - 'name' (str): Movie title.
            - 'director' (str): Movie director.
            - 'year' (int or None): Release year, if available and numeric.
            - 'poster_url' (str or None): URL of the movie poster, if available.

    Raises:
        ValueError: If the movie is not found or OMDB returns an error.
        requests.HTTPError: If the HTTP request fails.
    """
    resp = requests.get(OMDB_API_URL, params={"t": title, "apikey": OMDB_API_KEY}, timeout=6)
    resp.raise_for_status()
    data = resp.json()
    if data.get("Response") != "True":
        raise ValueError(data.get("Error", "Movie not found"))
    return {
        "name": data.get("Title"),
        "director": data.get("Director"),
        "year": int(data.get("Year")) if data.get("Year", "").isdigit() else None,
        "poster_url": data.get("Poster") if data.get("Poster") not in (None, "N/A") else None
    }
