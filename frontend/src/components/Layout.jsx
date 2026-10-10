import { useEffect, useState } from "react";
import { Link, NavLink, Outlet, useLocation } from "react-router-dom";
import { usePresentations } from "../PresentationsContext.jsx";

export default function Layout() {
  const [open, setOpen] = useState(false);
  const { presentations, loading, error } = usePresentations();
  const location = useLocation();

  useEffect(() => setOpen(false), [location.pathname]);

  return (
    <div className="app">
      <header className="header">
        <button
          className="icon-btn menu-btn"
          aria-label="Toggle sidebar"
          onClick={() => setOpen((o) => !o)}
        >
          ☰
        </button>
        <Link to="/" className="brand">
          <span className="brand-mark" aria-hidden="true" />
          FLUXA
        </Link>
        <span className="tagline">AI-powered dynamic presentations</span>
        <Link to="/create" className="btn btn-accent">+ New presentation</Link>
      </header>

      <div className="body">
        <aside className={`sidebar ${open ? "open" : ""}`} aria-label="Presentations">
          <h2>Your presentations</h2>
          {loading && <p className="muted">Loading…</p>}
          {error && <p className="error-text">{error}</p>}
          {!loading && !error && presentations.length === 0 && (
            <p className="muted">No presentations yet.</p>
          )}
          <nav>
            <ul>
              {presentations.map((p) => (
                <li key={p.id}>
                  <NavLink
                    to={`/presentations/${p.id}`}
                    className={({ isActive }) => `side-link ${isActive ? "active" : ""}`}
                  >
                    <span className="side-title">{p.title}</span>
                    <small>{p.slide_count} {p.slide_count === 1 ? "slide" : "slides"}</small>
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>
        </aside>

        <main className="content">
          <div key={location.pathname} className="page">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
