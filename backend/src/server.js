require("dotenv").config();
const express = require("express");
const cors = require("cors");

const connectDB = require("./config/db");
const presentationRoutes = require("./routes/presentations");

const app = express();
app.use(cors());
app.use(express.json());

// Base routing structure (T4)
app.use("/api/presentations", presentationRoutes);

app.get("/health", (req, res) => res.json({ status: "ok" }));

const PORT = process.env.PORT || 4000;
const MONGO_URI = process.env.MONGO_URI || "mongodb://localhost:27017/fluxa";

connectDB(MONGO_URI).then(() => {
  app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
});
