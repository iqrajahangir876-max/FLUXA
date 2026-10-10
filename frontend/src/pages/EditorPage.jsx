import { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../api.js";
import { usePresentations } from "../PresentationsContext.jsx";
import ConfirmButton from "../components/ConfirmButton.jsx";
import SlidePreview from "../components/SlidePreview.jsx";

export default function EditorPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { refresh } = usePresentations();

  const [presentation, setPresentation] = useState(null);
  const [slides, setSlides] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [drafts, setDrafts] = useState({}); // unsaved edits, keyed by slide id
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");

  const load = useCallback(
    async (preferId) => {
      try {
        const { presentation: p } = await api.getPresentation(id);
        setPresentation(p);
        setSlides(p.slides);
        const next = p.slides.find((s) => s.id === preferId) || p.slides[0] || null;
        setSelectedId(next ? next.id : null);
        setError("");
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    },
    [id]
  );

  useEffect(() => {
    setLoading(true);
    setDrafts({});
    load();
  }, [load]);

  const selected = slides.find((s) => s.id === selectedId) || null;
  const current = selected
    ? drafts[selected.id] || { title: selected.title || "", content: selected.content || "" }
    : null;
  const dirty =
    selected &&
    (current.title !== (selected.title || "") || current.content !== (selected.content || ""));

  function edit(field, value) {
    setStatus("");
    setDrafts((d) => ({ ...d, [selected.id]: { ...current, [field]: value } }));
  }

  async function run(action) {
    try {
      setError("");
      await action();
    } catch (err) {
      setError(err.message);
    }
  }

  const save = () =>
    run(async () => {
      const { slide } = await api.updateSlide(id, selected.id, current);
      setSlides((list) => list.map((s) => (s.id === slide.id ? slide : s)));
      setDrafts(({ [slide.id]: _removed, ...rest }) => rest);
      setStatus("Saved");
    });

  const addSlide = () =>
    run(async () => {
      const { slide } = await api.addSlide(id, { title: "Untitled slide", content: "" });
      await load(slide.id);
      await refresh();
    });

  const removeSlide = () =>
    run(async () => {
      const index = slides.findIndex((s) => s.id === selected.id);
      const neighbour = slides[index + 1] || slides[index - 1];
      await api.deleteSlide(id, selected.id);
      await load(neighbour ? neighbour.id : undefined);
      await refresh();
    });

  const removePresentation = () =>
    run(async () => {
      await api.deletePresentation(id);
      await refresh();
      navigate("/");
    });

  if (loading) return <p className="muted">Loading presentation…</p>;
  if (!presentation) return <p role="alert" className="error-text">{error}</p>;

  return (
    <div>
      <div className="page-head">
        <div>
          <h1>{presentation.title}</h1>
          {presentation.description && <p className="muted clamp">{presentation.description}</p>}
        </div>
        <ConfirmButton
          label="Delete presentation"
          onConfirm={removePresentation}
          className="btn btn-danger-outline"
        />
      </div>

      {error && <p role="alert" className="error-text">{error}</p>}

      <div className="editor-grid">
        <nav className="slide-rail" aria-label="Slides">
          <ol>
            {slides.map((s, i) => {
              const label = (drafts[s.id]?.title ?? s.title) || "Untitled slide";
              return (
                <li key={s.id}>
                  <button
                    type="button"
                    className={`thumb ${s.id === selectedId ? "active" : ""}`}
                    aria-current={s.id === selectedId ? "true" : undefined}
                    onClick={() => setSelectedId(s.id)}
                  >
                    <span className="thumb-num">{i + 1}</span>
                    <span className="thumb-title">{label}</span>
                  </button>
                </li>
              );
            })}
          </ol>
          <button type="button" className="btn btn-outline full" onClick={addSlide}>
            + Add slide
          </button>
        </nav>

        {selected ? (
          <section className="editor-pane">
            <form
              className="card form"
              onSubmit={(e) => {
                e.preventDefault();
                save();
              }}
            >
              <div className="field">
                <label htmlFor="slide-title">Slide title</label>
                <input
                  id="slide-title"
                  type="text"
                  value={current.title}
                  onChange={(e) => edit("title", e.target.value)}
                />
              </div>
              <div className="field">
                <label htmlFor="slide-content">Slide content</label>
                <textarea
                  id="slide-content"
                  rows={10}
                  value={current.content}
                  placeholder={"Write text, or start lines with “- ” for bullets"}
                  onChange={(e) => edit("content", e.target.value)}
                />
              </div>
              <div className="actions">
                <span className="muted status" aria-live="polite">
                  {dirty ? "Unsaved changes" : status}
                </span>
                <ConfirmButton
                  label="Delete slide"
                  onConfirm={removeSlide}
                  className="btn btn-danger-outline"
                />
                <button type="submit" className="btn" disabled={!dirty}>Save changes</button>
              </div>
            </form>

            <div className="card">
              <h3>Live preview</h3>
              <SlidePreview title={current.title} content={current.content} />
            </div>
          </section>
        ) : (
          <div className="empty">
            <h2>No slides yet</h2>
            <p className="muted">Add your first slide to get started.</p>
          </div>
        )}
      </div>
    </div>
  );
}
