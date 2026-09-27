const Presentation = require("../models/Presentation");

// T6: Create a new, empty (or seeded) presentation
async function createPresentation(req, res) {
  try {
    const { title, theme, slides } = req.body;

    if (!title || typeof title !== "string") {
      return res.status(400).json({ error: "A 'title' string is required." });
    }

    const presentation = await Presentation.create({
      title,
      theme: theme || "default",
      ownerId: req.user?.id, // set by your auth middleware
      slides: slides && slides.length
        ? slides
        : [
            {
              id: "slide-1",
              layout: "title",
              order: 0,
              components: [
                {
                  id: "comp-1",
                  type: "text",
                  position: { x: 40, y: 40, width: 600, height: 80 },
                  content: title,
                },
              ],
            },
          ],
    });

    return res.status(201).json(presentation);
  } catch (err) {
    console.error("createPresentation error:", err);
    return res.status(500).json({ error: "Failed to create presentation." });
  }
}

async function getPresentation(req, res) {
  try {
    const presentation = await Presentation.findById(req.params.id);
    if (!presentation) return res.status(404).json({ error: "Not found." });
    return res.json(presentation);
  } catch (err) {
    return res.status(500).json({ error: "Failed to fetch presentation." });
  }
}

async function listPresentations(req, res) {
  try {
    const presentations = await Presentation.find({ ownerId: req.user?.id })
      .select("title theme createdAt updatedAt")
      .sort({ updatedAt: -1 });
    return res.json(presentations);
  } catch (err) {
    return res.status(500).json({ error: "Failed to list presentations." });
  }
}

async function updatePresentation(req, res) {
  try {
    const updated = await Presentation.findByIdAndUpdate(
      req.params.id,
      { $set: req.body },
      { new: true, runValidators: true }
    );
    if (!updated) return res.status(404).json({ error: "Not found." });
    return res.json(updated);
  } catch (err) {
    return res.status(500).json({ error: "Failed to update presentation." });
  }
}

async function deletePresentation(req, res) {
  try {
    const deleted = await Presentation.findByIdAndDelete(req.params.id);
    if (!deleted) return res.status(404).json({ error: "Not found." });
    return res.status(204).send();
  } catch (err) {
    return res.status(500).json({ error: "Failed to delete presentation." });
  }
}

module.exports = {
  createPresentation,
  getPresentation,
  listPresentations,
  updatePresentation,
  deletePresentation,
};
