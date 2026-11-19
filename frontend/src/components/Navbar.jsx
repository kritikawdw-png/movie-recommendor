
import { Film, Search, Sun, Moon } from "lucide-react";

function Navbar({ darkMode, setDarkMode }) {
  return (
    <nav className="navbar">
      <div className="logo">
        <Film size={27} />
        <span>CINEPHILE</span>
      </div>

      <div className="nav-links">
        <a href="/">Home</a>
        <a href="/search">Explore</a>
        <a href="/recommendations">Recommendations</a>
      </div>

      <div className="nav-actions">
        <a href="/search" className="search-icon" aria-label="Search">
          <Search size={21} />
        </a>

        <button
          className="theme-button"
          onClick={() => setDarkMode(!darkMode)}
          aria-label="Toggle theme"
        >
          {darkMode ? <Sun size={20} /> : <Moon size={20} />}
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
