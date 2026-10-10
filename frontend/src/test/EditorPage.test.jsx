import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import App from "../App.jsx";
import { mockApi } from "./mockApi.js";

const slide = (id, order, title, content) => ({
  id,
  presentation_id: 3,
  slide_order: order,
  title,
  content,
});

const handlers = () => ({
  "GET /api/presentations": {
    body: { count: 1, presentations: [{ id: 3, title: "Deck", description: "", slide_count: 2 }] },
  },
  "GET /api/presentations/3": {
    body: {
      presentation: {
        id: 3,
        title: "Deck",
        description: "",
        slide_count: 2,
        slides: [slide(10, 1, "Intro", "Hello"), slide(11, 2, "Outro", "Bye")],
      },
    },
  },
});

function renderEditor() {
  return render(
    <MemoryRouter initialEntries={["/presentations/3"]}>
      <App />
    </MemoryRouter>
  );
}

test("loads slides, selects the first and shows a live preview", async () => {
  mockApi(handlers());
  renderEditor();

  expect(await screen.findByLabelText(/slide title/i)).toHaveValue("Intro");
  expect(screen.getByLabelText(/slide content/i)).toHaveValue("Hello");

  const rail = screen.getByRole("navigation", { name: /slides/i });
  expect(within(rail).getAllByRole("button", { name: /Intro|Outro/ })).toHaveLength(2);

  expect(within(screen.getByTestId("slide-preview")).getByText("Hello")).toBeInTheDocument();
});

test("editing updates the preview and Save sends a PUT request", async () => {
  const calls = mockApi({
    ...handlers(),
    "PUT /api/presentations/3/slides/10": (call) => ({
      body: { slide: slide(10, 1, call.body.title, call.body.content) },
    }),
  });
  renderEditor();

  const content = await screen.findByLabelText(/slide content/i);
  const save = screen.getByRole("button", { name: /save changes/i });
  expect(save).toBeDisabled();

  await userEvent.clear(content);
  await userEvent.type(content, "New text");

  expect(within(screen.getByTestId("slide-preview")).getByText("New text")).toBeInTheDocument();
  expect(screen.getByText(/unsaved changes/i)).toBeInTheDocument();

  await userEvent.click(save);

  expect(await screen.findByText("Saved")).toBeInTheDocument();
  const put = calls.find((c) => c.method === "PUT");
  expect(put.body).toEqual({ title: "Intro", content: "New text" });
});

test("switching slides keeps unsaved edits", async () => {
  mockApi(handlers());
  renderEditor();

  const title = await screen.findByLabelText(/slide title/i);
  await userEvent.type(title, "!");

  const rail = screen.getByRole("navigation", { name: /slides/i });
  await userEvent.click(within(rail).getByRole("button", { name: /Outro/ }));
  expect(screen.getByLabelText(/slide title/i)).toHaveValue("Outro");

  await userEvent.click(within(rail).getByRole("button", { name: /Intro!/ }));
  expect(screen.getByLabelText(/slide title/i)).toHaveValue("Intro!");
});

test("Add slide sends a POST request", async () => {
  const calls = mockApi({
    ...handlers(),
    "POST /api/presentations/3/slides": { status: 201, body: { slide: slide(12, 3, "Untitled slide", "") } },
  });
  renderEditor();

  await userEvent.click(await screen.findByRole("button", { name: /add slide/i }));

  await screen.findByLabelText(/slide title/i);
  const post = calls.find((c) => c.method === "POST");
  expect(post.url).toBe("/api/presentations/3/slides");
  expect(post.body).toEqual({ title: "Untitled slide", content: "" });
});

test("deleting a slide needs a second confirming click", async () => {
  const calls = mockApi({
    ...handlers(),
    "DELETE /api/presentations/3/slides/10": { body: { message: "Slide deleted successfully" } },
  });
  renderEditor();

  await userEvent.click(await screen.findByRole("button", { name: "Delete slide" }));
  expect(calls.some((c) => c.method === "DELETE")).toBe(false);

  await userEvent.click(screen.getByRole("button", { name: "Confirm delete" }));

  await screen.findByLabelText(/slide title/i);
  expect(calls.some((c) => c.method === "DELETE" && c.url.endsWith("/slides/10"))).toBe(true);
});

test("shows an error when the presentation does not exist", async () => {
  mockApi({
    "GET /api/presentations": { body: { count: 0, presentations: [] } },
    "GET /api/presentations/3": { status: 404, body: { error: "Presentation not found." } },
  });
  renderEditor();

  expect(await screen.findByText("Presentation not found.")).toBeInTheDocument();
});
