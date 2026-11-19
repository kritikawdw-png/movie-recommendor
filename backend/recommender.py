
import pickle
from pathlib import Path

# Find the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the existing ML files
with open(BASE_DIR / "movies.pkl", "rb") as file:
    movies = pickle.load(file)

with open(BASE_DIR / "similaritity.pkl", "rb") as file:
    similarity = pickle.load(file)


def get_all_movies():
    """Return the movie titles and IDs."""

    return [
        {
            "movie_id": int(row.movie_id),
            "title": str(row.title)
        }
        for row in movies[["movie_id", "title"]]
        .drop_duplicates(subset=["movie_id"])
        .itertuples(index=False)
    ]


def search_movies(query):
    """Search movies by title."""

    if not query.strip():
        return []

    results = movies[
        movies["title"].str.contains(
            query,
            case=False,
            na=False
        )
    ].drop_duplicates(subset=["movie_id"]).head(20)

    return [
        {
            "movie_id": int(row.movie_id),
            "title": str(row.title)
        }
        for row in results.itertuples(index=False)
    ]


def get_recommendations(movie_title, limit=5):
    """Recommend similar movies using the existing similarity matrix."""

    matching_movies = movies[
        movies["title"].str.lower() == movie_title.strip().lower()
    ]

    if matching_movies.empty:
        return None

    movie_index = matching_movies.index[0]

    distances = similarity[movie_index]

    movie_indices = sorted(
        enumerate(distances),
        key=lambda x: x[1],
        reverse=True
    )[1:limit + 1]

    recommendations = []

    for index, score in movie_indices:
        movie = movies.iloc[index]

        recommendations.append({
            "movie_id": int(movie["movie_id"]),
            "title": str(movie["title"]),
            "similarity_score": float(score)
        })

    return recommendations

print("MOVIE DATASET COLUMNS:")
print(movies.columns.tolist())

print("\nFIRST 10 MOVIES:")
print(movies[["movie_id", "title"]].head(10))

print("\nMOVIE ID EXAMPLES:")
print(movies["movie_id"].head(10).tolist())

