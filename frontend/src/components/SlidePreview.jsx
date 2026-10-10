const BULLET = /^[-•*]\s+/;

export default function SlidePreview({ title, content }) {
  const lines = (content || "").split("\n").filter((line) => line.trim() !== "");

  return (
    <div className="preview" data-testid="slide-preview">
      <div className="preview-inner">
        <h2>{title || "Untitled slide"}</h2>
        <div className="preview-body">
          {lines.map((line, i) =>
            BULLET.test(line) ? (
              <p key={i} className="bullet">{line.replace(BULLET, "")}</p>
            ) : (
              <p key={i}>{line}</p>
            )
          )}
        </div>
      </div>
    </div>
  );
}
