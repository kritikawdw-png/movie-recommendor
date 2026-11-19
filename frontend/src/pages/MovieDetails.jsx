

import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getMovieDetails, getSimilarMovies } from "../services/api";

function MovieDetails() {
  const { movieId } = useParams();

  const [movie, setMovie] = useState(null);
  const [similarMovies, setSimilarMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadMovie() {
      setLoading(true);
      setError("");
      setMovie(null);
      setSimilarMovies([]);

      try {
        const movieData = await getMovieDetails(movieId);
        setMovie(movieData);

        // Load recommendations separately
        try {
          const recommendations = await getSimilarMovies(movieData.title);
          setSimilarMovies(recommendations.recommendations || []);
        } catch (err) {
          console.log("No similar movies available for this title.");
          setSimilarMovies([]);
        }

      } catch (err) {
        console.error("Movie details error:", err);
        setError("Unable to load movie details. Please try again.");
      } finally {
        setLoading(false);
      }
    }

    loadMovie();
  }, [movieId]);

  if (loading) {
    return <p className="status-message">Loading movie details...</p>;
  }

  if (error) {
    return <p className="error-message">{error}</p>;
  }

  if (!movie) {
    return <p>Movie not found.</p>;
  }

  return (
    <main className="details-page">

      <section className="movie-details">

        <img
          className="details-poster"
          src={movie.poster}
          alt={movie.title}
        />

        <div className="details-info">

          <h1>{movie.title}</h1>

          <p className="details-rating">
            ⭐ {movie.rating?.toFixed(1) || "N/A"} / 10
          </p>

          <p>
            <strong>Release Date:</strong>{" "}
            {movie.release_date || "N/A"}
          </p>

          <p>
            <strong>Runtime:</strong>{" "}
            {movie.runtime ? `${movie.runtime} minutes` : "N/A"}
          </p>

          <p>
            <strong>Director:</strong>{" "}
            {movie.director || "N/A"}
          </p>

          <p>
            <strong>Genres:</strong>{" "}
            {movie.genres?.join(", ") || "N/A"}
          </p>

          <h2>Overview</h2>

          <p className="movie-overview">
            {movie.overview || "No overview available."}
          </p>

          <h2>Cast</h2>

          <p>
            {movie.cast?.map((person) => person.name).join(", ") ||
              "Cast information unavailable."}
          </p>

        </div>
      </section>

      <section className="movie-section">

        <h2>You May Also Like</h2>

        {similarMovies.length > 0 ? (
          <div className="movie-grid">
            {similarMovies.map((item) => (
              <article className="movie-card" key={item.movie_id}>
                <h3>{item.title}</h3>
                {item.similarity_score !== undefined && (
                  <p>
                    Similarity: {(item.similarity_score * 100).toFixed(1)}%
                  </p>
                )}
              </article>
            ))}
          </div>
        ) : (
          <p className="status-message">
            Recommendations are not available for this movie yet.
          </p>
        )}

      </section>

    </main>
  );
}

export default MovieDetails;
