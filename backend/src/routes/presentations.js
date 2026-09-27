const express = require("express");
const router = express.Router();

const {
  createPresentation,
  getPresentation,
  listPresentations,
  updatePresentation,
  deletePresentation,
} = require("../controllers/presentationController");

// const requireAuth = require("../middleware/requireAuth");
// router.use(requireAuth); // 

router.get("/", listPresentations);          // GET    /api/presentations
router.post("/", createPresentation);        // POST   /api/presentations
router.get("/:id", getPresentation);         // GET    /api/presentations/:id
router.put("/:id", updatePresentation);      // PUT    /api/presentations/:id
router.delete("/:id", deletePresentation);   // DELETE /api/presentations/:id

module.exports = router;
