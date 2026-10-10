import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api.js";
import { usePresentations } from "../PresentationsContext.jsx";
import PromptInput from "../components/PromptInput.jsx";

export default function CreatePresentation() {
  const navigate = useNavigate();
  const { refresh } = usePresentations();
  const [title, setTitle] = useState("");
  const [prompt, setPrompt] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    const cleanPrompt = prompt.trim();
    const cleanTitle = title.trim() || cleanPrompt.slice(0, 60);

    if (!cleanTitle) {
      setError("Enter a title or describe your topic to continue.");
      return;
    }

    setBusy(true);
    setError("");

    try {
      const { presentation } = await api.createPresentation({
        title: cleanTitle,
        description: cleanPrompt,
      });
      // Start every presentation with a title slide
      await api.addSlide(presentation.id, { title: cleanTitle, content: cleanPrompt });
      await refresh();
      navigate(`/presentations/${presentation.id}`);
    } catch (err) {
      setError(err.message);
      setBusy(false);
    }
  }

  return (
    <div className="narrow">
      <h1>New presentation</h1>
      <p className="muted">Start with a topic. You can edit every slide afterwards.</p>

      <form className="card form" onSubmit={handleSubmit} noValidate>
        <div className="field">
          <label htmlFor="title">Title (optional)</label>
          <input
            id="title"
            type="text"
            value={title}
            disabled={busy}
            maxLength={120}
            placeholder="Leave empty to use your topic"
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <PromptInput value={prompt} onChange={setPrompt} disabled={busy} />

        {error && <p role="alert" className="error-text">{error}</p>}

        <div className="actions">
          <button type="button" className="btn btn-outline" onClick={() => navigate("/")} disabled={busy}>
            Cancel
          </button>
          <button type="submit" className="btn" disabled={busy}>
            {busy ? "Creating…" : "Create presentation"}
          </button>
        </div>
      </form>
    </div>
  );
}
