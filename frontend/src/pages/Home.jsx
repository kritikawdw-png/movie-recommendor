import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { getTrendingMovies, getPopularMovies } from "../services/api";

function Home() {
  const [trending, setTrending] = useState([]);
  const [popular, setPopular] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadMovies() {
      try {
        const [trendingData, popularData] = await Promise.all([
          getTrendingMovies(),
          getPopularMovies(),
        ]);

        setTrending(trendingData.movies || []);
        setPopular(popularData.movies || []);
      } catch (err) {
        setError("Unable to load movies. Please check your backend.");
      } finally {
        setLoading(false);
      }
    }

    loadMovies();
  }, []);

  return (
    <main className="home-page">
      <section className="hero">
        <p className="hero-label">YOUR WORLD OF CINEMA</p>
        <h1>Discover stories<br />worth remembering.</h1>
        <p className="hero-description">
          Explore movies, find hidden gems and discover your next favourite film.
        </p>
      </section>

      {loading && <p className="status-message">Loading movies...</p>}

      {error && <p className="error-message">{error}</p>}

      {!loading && !error && (
        <>
          <MovieSection title="Trending This Week" movies={trending} />
          <MovieSection title="Popular Movies" movies={popular} />
        </>
      )}
    </main>
  );
}

function MovieSection({ title, movies }) {
  return (
    <section className="movie-section">
      <h2>{title}</h2>

      <div className="movie-grid">
        {movies.map((movie) => (
          <Link
              to={`/movie/${movie.movie_id}`}
              className="movie-card"
              key={movie.movie_id}
          >
            {movie.poster ? (
                <img src={movie.poster} alt={movie.title} />
            ) : (
                <div className="poster-placeholder">No poster</div>
            )}
            <div className="movie-info">
              <h3>{movie.title}</h3>
              <p>⭐ {movie.rating?.toFixed(1) || "N/A"}</p>
              <p>{movie.release_date || "Release date unavailable"}</p>
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}

export default Home;
