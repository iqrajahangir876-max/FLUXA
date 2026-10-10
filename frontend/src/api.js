async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`/api${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch {
    throw new Error("Cannot reach the server. Is the backend running?");
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Something went wrong.");
  }
  return data;
}

const send = (method, body) => ({
  method,
  body: body === undefined ? undefined : JSON.stringify(body),
});

export const api = {
  listPresentations: () => request("/presentations"),
  getPresentation: (id) => request(`/presentations/${id}`),
  createPresentation: (body) => request("/presentations", send("POST", body)),
  deletePresentation: (id) => request(`/presentations/${id}`, send("DELETE")),
  addSlide: (pid, body) => request(`/presentations/${pid}/slides`, send("POST", body)),
  updateSlide: (pid, sid, body) =>
    request(`/presentations/${pid}/slides/${sid}`, send("PUT", body)),
  deleteSlide: (pid, sid) => request(`/presentations/${pid}/slides/${sid}`, send("DELETE")),
};
