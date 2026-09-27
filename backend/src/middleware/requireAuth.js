
function requireAuth(req, res, next) {
  const token = req.headers.authorization?.split(" ")[1];

  if (!token) {
    return res.status(401).json({ error: "Missing auth token." });
  }

  req.user = { id: "placeholder-user-id" };

  next();
}

module.exports = requireAuth;
