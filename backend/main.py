import os
from tmdb import (
    get_movie_details,
    get_trending_movies,
    get_popular_movies,
    get_movie_poster
)
import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from recommender import (
    get_all_movies,
    search_movies,
    get_recommendations
)

app = FastAPI(
    title="Cinephile API",
    description="Movie discovery and recommendation backend",
    version="1.0.0"
)

# Allow React frontend to communicate with FastAPI
FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Cinephile API!",
        "status": "running"
    }


@app.get("/movies")
def movies_list(limit: int = Query(default=50, ge=1, le=500)):
    return {
        "movies": get_all_movies()[:limit]
    }


@app.get("/search")
def search(q: str = Query(min_length=1)):
    results = search_movies(q)

    return {
        "query": q,
        "total": len(results),
        "results": results
    }



@app.get("/recommend/similar")
def recommend(movie: str, limit: int = Query(default=5, ge=1, le=20)):
    results = get_recommendations(movie, limit)

    if results is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    for item in results:
        try:
            item["poster"] = get_movie_poster(item["movie_id"])
        except requests.exceptions.RequestException:
            item["poster"] = None

    return {
        "selected_movie": movie,
        "recommendations": results
    }

@app.get("/movie/{movie_id}")
def movie_details(movie_id: int):

    try:
        details = get_movie_details(movie_id)
        return details

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response is not None else 502

        raise HTTPException(
            status_code=502,
            detail=f"TMDB API error: {status_code}"
        )

    except requests.exceptions.RequestException as e:
        print("TMDB CONNECTION ERROR:", repr(e))
        raise HTTPException(
            status_code=502,
            detail=f"TMDB connection error: {repr(e)}"
        )
@app.get("/trending")
def trending():
    try:
        return {"movies": get_trending_movies()}
    except Exception as e:
        print("TRENDING ERROR:", repr(e))
        raise HTTPException(status_code=502, detail=str(e))


@app.get("/popular")
def popular():
    try:
        return {"movies": get_popular_movies()}
    except Exception as e:
        print("POPULAR ERROR:", repr(e))
        raise HTTPException(status_code=502, detail=str(e))