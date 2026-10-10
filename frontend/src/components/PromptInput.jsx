export const MAX_PROMPT = 2000;

const EXAMPLES = [
  "Introduction to machine learning",
  "Q4 marketing strategy",
  "Climate change solutions",
  "Startup pitch for a food-delivery app",
];

export default function PromptInput({ value, onChange, disabled = false }) {
  return (
    <div className="field">
      <label htmlFor="prompt">Topic or prompt</label>
      <textarea
        id="prompt"
        rows={5}
        value={value}
        maxLength={MAX_PROMPT}
        disabled={disabled}
        placeholder="Describe what your presentation should cover…"
        onChange={(e) => onChange(e.target.value)}
      />
      <div className="field-row">
        <div className="chips" role="group" aria-label="Example prompts">
          {EXAMPLES.map((example) => (
            <button
              key={example}
              type="button"
              className="chip"
              disabled={disabled}
              onClick={() => onChange(example)}
            >
              {example}
            </button>
          ))}
        </div>
        <span className="muted" data-testid="char-count">
          {value.length}/{MAX_PROMPT}
        </span>
      </div>
    </div>
  );
}
