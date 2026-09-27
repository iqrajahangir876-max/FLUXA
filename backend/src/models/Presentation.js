const mongoose = require("mongoose");
const { Schema } = mongoose;

const ComponentSchema = new Schema(
  {
    id: { type: String, required: true },
    type: {
      type: String,
      enum: ["text", "image", "shape", "chart", "timeline", "video", "embed"],
      required: true,
    },
    position: {
      x: { type: Number, default: 0 },
      y: { type: Number, default: 0 },
      width: { type: Number, default: 100 },
      height: { type: Number, default: 100 },
    },
    style: { type: Schema.Types.Mixed, default: {} }, 
    content: { type: Schema.Types.Mixed }, 
    data: { type: Schema.Types.Mixed }, 
    interactions: { type: Schema.Types.Mixed, default: {} }, 
    animation: {
      type: { type: String, default: "none" }, 
      duration: { type: Number, default: 500 },
      delay: { type: Number, default: 0 },
    },
  },
  { _id: false }
);

const SlideSchema = new Schema(
  {
    id: { type: String, required: true },
    layout: { type: String, default: "blank" }, // title, title-content, two-column...
    background: { type: Schema.Types.Mixed, default: {} },
    components: { type: [ComponentSchema], default: [] },
    transition: { type: String, default: "slide" }, // maps to reveal.js transitions
    notes: { type: String, default: "" },
    order: { type: Number, required: true },
  },
  { _id: false }
);

const PresentationSchema = new Schema(
  {
    title: { type: String, required: true, trim: true },
    ownerId: { type: Schema.Types.ObjectId, ref: "User" },
    theme: { type: String, default: "default" },
    slides: { type: [SlideSchema], default: [] },
    isPublic: { type: Boolean, default: false },
  },
  { timestamps: true } 
);

module.exports = mongoose.model("Presentation", PresentationSchema);
