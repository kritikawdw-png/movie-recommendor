
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function fetchAPI(endpoint) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }

  return response.json();
}

export function getTrendingMovies() {
  return fetchAPI("/trending");
}

export function getPopularMovies() {
  return fetchAPI("/popular");
}

export function searchMovies(query) {
  return fetchAPI(`/search?q=${encodeURIComponent(query)}`);
}

export function getMovieDetails(movieId) {
  return fetchAPI(`/movie/${movieId}`);
}

export function getSimilarMovies(movieTitle) {
  return fetchAPI(
    `/recommend/similar?movie=${encodeURIComponent(movieTitle)}`
  );
}
