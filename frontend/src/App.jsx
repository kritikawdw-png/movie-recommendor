import MovieDetails from "./pages/MovieDetails";
import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Home from "./pages/Home";

import "./App.css";

function App() {
  const [darkMode, setDarkMode] = useState(true);

  return (
    <BrowserRouter>
      <div className={darkMode ? "app-shell dark" : "app-shell light"}>
        <Navbar
          darkMode={darkMode}
          setDarkMode={setDarkMode}
        />

        <Routes>
          <Route path="/movie/:movieId" element={<MovieDetails />} />
          <Route path="/" element={<Home />} />

          <Route
            path="/search"
            element={<div className="placeholder-page">Search page coming soon...</div>}
          />

          <Route
            path="/recommendations"
            element={<div className="placeholder-page">Recommendations coming soon...</div>}
          />

          <Route
            path="*"
            element={<div className="placeholder-page">Page not found.</div>}
          />
        </Routes>

        <footer className="footer">
          <p>© 2026 CINEPHILE. Made for movie lovers.</p>
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;
