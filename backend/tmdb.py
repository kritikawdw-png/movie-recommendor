
import os
import json
import time
import hashlib
from pathlib import Path

import requests
from dotenv import load_dotenv


# ----------------------------------
# Configuration
# ----------------------------------

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")
BASE_URL = "https://api.themoviedb.org/3"

CACHE_DIR = BASE_DIR / ".cache" / "tmdb"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

SESSION = requests.Session()

HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
}


# ----------------------------------
# Cache functions
# ----------------------------------

def get_cache_path(endpoint, params):
    cache_key = json.dumps(
        {"endpoint": endpoint, "params": params or {}},
        sort_keys=True
    )

    filename = hashlib.sha256(
        cache_key.encode("utf-8")
    ).hexdigest() + ".json"

    return CACHE_DIR / filename


def read_cache(cache_path):
    if not cache_path.exists():
        return None

    try:
        with open(cache_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return None


def save_cache(cache_path, data):
    temporary_path = cache_path.with_suffix(".tmp")

    try:
        with open(temporary_path, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "saved_at": time.time(),
                    "data": data
                },
                file
            )

        temporary_path.replace(cache_path)

    except OSError as error:
        print("CACHE SAVE ERROR:", repr(error))


# ----------------------------------
# Central TMDB request function
# ----------------------------------

def tmdb_get(endpoint, params=None, cache_hours=24):
    if not TMDB_ACCESS_TOKEN:
        raise RuntimeError(
            "TMDB access token is missing. Check backend/.env"
        )

    params = params or {}
    cache_path = get_cache_path(endpoint, params)
    cached = read_cache(cache_path)

    # Use fresh cache without contacting TMDB
    if cached:
        age = time.time() - cached.get("saved_at", 0)

        if age < cache_hours * 3600:
            print("TMDB CACHE HIT:", endpoint)
            return cached["data"]

    url = f"{BASE_URL}{endpoint}"

    # Three attempts with increasing delays
    for attempt in range(3):
        try:
            response = SESSION.get(
                url,
                headers=HEADERS,
                params=params,
                timeout=(10, 30)
            )

            response.raise_for_status()

            data = response.json()

            save_cache(cache_path, data)

            print("TMDB LIVE DATA:", endpoint)

            return data

        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout
        ) as error:

            print(
                f"TMDB CONNECTION ATTEMPT {attempt + 1}/3:",
                repr(error)
            )

            if attempt < 2:
                time.sleep(2 ** attempt)

        except requests.exceptions.HTTPError as error:

            status = (
                error.response.status_code
                if error.response is not None
                else 0
            )

            print("TMDB HTTP ERROR:", status)

            # Retry only temporary server/rate-limit errors
            if status not in (429, 500, 502, 503, 504):
                raise

            if attempt < 2:
                time.sleep(2 ** attempt)

    # All attempts failed. Use previously cached data,
    # even if it has expired.
    if cached:
        print("TMDB OFFLINE: USING OLD CACHE:", endpoint)
        return cached["data"]

    raise requests.exceptions.ConnectionError(
        f"TMDB unavailable and no cached data exists for {endpoint}"
    )


# ----------------------------------
# Movie formatting
# ----------------------------------

def format_movie_list(movies):
    return [
        {
            "movie_id": movie.get("id"),
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "rating": movie.get("vote_average"),
            "release_date": movie.get("release_date"),
            "poster": (
                f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                if movie.get("poster_path") else None
            ),
            "backdrop": (
                f"https://image.tmdb.org/t/p/w1280{movie['backdrop_path']}"
                if movie.get("backdrop_path") else None
            )
        }
        for movie in movies
    ]


# ----------------------------------
# Trending movies
# ----------------------------------

def get_trending_movies():
    data = tmdb_get(
        "/trending/movie/week",
        cache_hours=1
    )

    return format_movie_list(data.get("results", []))


# ----------------------------------
# Popular movies
# ----------------------------------

def get_popular_movies():
    data = tmdb_get(
        "/movie/popular",
        cache_hours=6
    )

    return format_movie_list(data.get("results", []))


# ----------------------------------
# Movie details
# ----------------------------------

def get_movie_details(movie_id):
    data = tmdb_get(
        f"/movie/{movie_id}",
        params={"append_to_response": "credits"},
        cache_hours=24 * 7
    )

    director = next(
        (
            person["name"]
            for person in data.get("credits", {}).get("crew", [])
            if person.get("job") == "Director"
        ),
        None
    )

    cast = [
        {
            "name": person["name"],
            "character": person.get("character")
        }
        for person in data.get("credits", {}).get("cast", [])[:10]
    ]

    return {
        "movie_id": data.get("id"),
        "title": data.get("title"),
        "original_title": data.get("original_title"),
        "overview": data.get("overview"),
        "release_date": data.get("release_date"),
        "rating": data.get("vote_average"),
        "runtime": data.get("runtime"),
        "genres": [
            genre["name"]
            for genre in data.get("genres", [])
        ],
        "poster": (
            f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
            if data.get("poster_path") else None
        ),
        "backdrop": (
            f"https://image.tmdb.org/t/p/w1280{data['backdrop_path']}"
            if data.get("backdrop_path") else None
        ),
        "director": director,
        "cast": cast
    }


# ----------------------------------
# Recommendation movie posters
# ----------------------------------

def get_movie_poster(movie_id):
    data = tmdb_get(
        f"/movie/{movie_id}",
        cache_hours=24 * 7
    )

    poster_path = data.get("poster_path")

    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"

    return None
