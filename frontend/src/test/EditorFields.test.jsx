import { render, screen } from "@testing-library/react";
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

function setup(extra = {}) {
  const calls = mockApi({
    "GET /api/presentations": {
      body: { count: 1, presentations: [{ id: 3, title: "Deck", description: "", slide_count: 1 }] },
    },
    "GET /api/presentations/3": {
      body: {
        presentation: {
          id: 3,
          title: "Deck",
          description: "",
          slide_count: 1,
          slides: [slide(10, 1, "Intro", "Hello")],
        },
      },
    },
    ...extra,
  });
  render(
    <MemoryRouter initialEntries={["/presentations/3"]}>
      <App />
    </MemoryRouter>
  );
  return calls;
}

test("shows the character count of the slide content", async () => {
  setup();
  expect(await screen.findByTestId("content-count")).toHaveTextContent("5 characters");

  await userEvent.type(screen.getByLabelText(/slide content/i), "!!");
  expect(screen.getByTestId("content-count")).toHaveTextContent("7 characters");
});

test("Discard changes is disabled until something is edited", async () => {
  setup();
  expect(await screen.findByRole("button", { name: /discard changes/i })).toBeDisabled();
});

test("Discard changes restores the saved text", async () => {
  setup();
  const title = await screen.findByLabelText(/slide title/i);
  await userEvent.type(title, " extra");
  expect(title).toHaveValue("Intro extra");

  await userEvent.click(screen.getByRole("button", { name: /discard changes/i }));

  expect(screen.getByLabelText(/slide title/i)).toHaveValue("Intro");
  expect(screen.getByRole("button", { name: /save changes/i })).toBeDisabled();
});

test("Ctrl+S saves the current slide", async () => {
  const calls = setup({
    "PUT /api/presentations/3/slides/10": (call) => ({
      body: { slide: slide(10, 1, call.body.title, call.body.content) },
    }),
  });
  const content = await screen.findByLabelText(/slide content/i);
  await userEvent.type(content, " world");

  await userEvent.keyboard("{Control>}s{/Control}");

  expect(await screen.findByText("Saved")).toBeInTheDocument();
  const put = calls.find((c) => c.method === "PUT");
  expect(put.body).toEqual({ title: "Intro", content: "Hello world" });
});

test("warns before leaving the page only when there are unsaved changes", async () => {
  setup();
  const content = await screen.findByLabelText(/slide content/i);

  const clean = new Event("beforeunload", { cancelable: true });
  window.dispatchEvent(clean);
  expect(clean.defaultPrevented).toBe(false);

  await userEvent.type(content, "!");

  const dirty = new Event("beforeunload", { cancelable: true });
  window.dispatchEvent(dirty);
  expect(dirty.defaultPrevented).toBe(true);
});