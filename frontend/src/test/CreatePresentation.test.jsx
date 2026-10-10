import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import App from "../App.jsx";
import { mockApi } from "./mockApi.js";

function renderCreate() {
  return render(
    <MemoryRouter initialEntries={["/create"]}>
      <App />
    </MemoryRouter>
  );
}

const baseHandlers = {
  "GET /api/presentations": { body: { count: 0, presentations: [] } },
};

test("an example chip fills the prompt and updates the counter", async () => {
  mockApi(baseHandlers);
  renderCreate();

  await userEvent.click(screen.getByRole("button", { name: "Q4 marketing strategy" }));

  expect(screen.getByLabelText(/topic or prompt/i)).toHaveValue("Q4 marketing strategy");
  expect(screen.getByTestId("char-count")).toHaveTextContent("21/2000");
});

test("shows a validation error when title and prompt are both empty", async () => {
  const calls = mockApi(baseHandlers);
  renderCreate();

  await userEvent.click(screen.getByRole("button", { name: /create presentation/i }));

  expect(screen.getByRole("alert")).toHaveTextContent(/enter a title or describe your topic/i);
  expect(calls.some((c) => c.method === "POST")).toBe(false);
});

test("creates the presentation, adds a title slide and opens the editor", async () => {
  const calls = mockApi({
    ...baseHandlers,
    "POST /api/presentations": {
      status: 201,
      body: { presentation: { id: 7, title: "AI basics" } },
    },
    "POST /api/presentations/7/slides": { status: 201, body: { slide: { id: 1 } } },
    "GET /api/presentations/7": {
      body: {
        presentation: { id: 7, title: "AI basics", description: "AI basics", slide_count: 0, slides: [] },
      },
    },
  });
  renderCreate();

  await userEvent.type(screen.getByLabelText(/topic or prompt/i), "AI basics");
  await userEvent.click(screen.getByRole("button", { name: /create presentation/i }));

  expect(await screen.findByRole("heading", { level: 1, name: "AI basics" })).toBeInTheDocument();

  const create = calls.find((c) => c.method === "POST" && c.url === "/api/presentations");
  expect(create.body).toEqual({ title: "AI basics", description: "AI basics" });
});

test("shows the server error when creation fails", async () => {
  mockApi({
    ...baseHandlers,
    "POST /api/presentations": { status: 400, body: { error: "Title is invalid." } },
  });
  renderCreate();

  await userEvent.type(screen.getByLabelText(/title/i), "Broken");
  await userEvent.click(screen.getByRole("button", { name: /create presentation/i }));

  expect(await screen.findByRole("alert")).toHaveTextContent("Title is invalid.");
});
