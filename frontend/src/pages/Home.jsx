import { Link } from "react-router-dom";
import { usePresentations } from "../PresentationsContext.jsx";

export default function Home() {
  const { presentations, loading } = usePresentations();

  return (
    <div>
      <section className="hero">
        <h1>Turn ideas into presentations</h1>
        <p className="muted">
          Describe a topic, then shape each slide with a clean editor and a live preview.
        </p>
        <Link to="/create" className="btn btn-accent">Create presentation</Link>
      </section>

      {!loading && presentations.length > 0 && (
        <section>
          <h2 className="section-title">Recent presentations</h2>
          <div className="card-grid">
            {presentations.map((p) => (
              <Link key={p.id} to={`/presentations/${p.id}`} className="card card-link">
                <h3>{p.title}</h3>
                <p className="muted clamp">{p.description || "No description"}</p>
                <small>{p.slide_count} {p.slide_count === 1 ? "slide" : "slides"}</small>
              </Link>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
