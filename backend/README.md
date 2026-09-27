# Fluxa Backend — Presentation API (KAN-6)

Implements:
- **T4** — base API routing structure (`src/routes/presentations.js`)
- **T5** — presentation data model (`src/models/Presentation.js`)
- **T6** — create-presentation endpoint (`src/controllers/presentationController.js`)

## Setup

```bash
npm install
cp .env.example .env      # then fill in MONGO_URI if not using local Mongo
npm run dev
```

Server starts on `http://localhost:4000` (or your `PORT`).

## Test it

```bash
curl -X POST http://localhost:4000/api/presentations \
  -H "Content-Type: application/json" \
  -d '{"title":"My First Deck"}'
```

## Folder structure

```
src/
├── config/db.js                 Mongo connection
├── models/Presentation.js       T5 — schema for slides/components/data
├── controllers/
│   └── presentationController.js  T6 — CRUD logic
├── routes/presentations.js      T4 — route definitions
├── middleware/requireAuth.js    placeholder auth, wire up when ready
└── server.js                    entry point
```

## Notes

- `requireAuth` is a stub — replace the token verification with real JWT
  (or your auth provider) logic before relying on `req.user`.
- `content` and `data` fields on components are `Mixed` type since they vary
  by component (text vs. chart vs. timeline) — validate shape at the API
  layer if you need stricter guarantees.
