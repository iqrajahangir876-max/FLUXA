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

function setup() {
  mockApi({
    "GET /api/presentations": {
      body: { count: 1, presentations: [{ id: 3, title: "Deck", description: "", slide_count: 3 }] },
    },
    "GET /api/presentations/3": {
      body: {
        presentation: {
          id: 3,
          title: "Deck",
          description: "",
          slide_count: 3,
          slides: [slide(10, 1, "One", "a"), slide(11, 2, "Two", "b"), slide(12, 3, "Three", "c")],
        },
      },
    },
  });
  return render(
    <MemoryRouter initialEntries={["/presentations/3"]}>
      <App />
    </MemoryRouter>
  );
}

test("shows the current slide position", async () => {
  setup();
  expect(await screen.findByTestId("slide-position")).toHaveTextContent("Slide 1 of 3");
});

test("Previous is disabled on the first slide and Next moves forward", async () => {
  setup();
  const prev = await screen.findByRole("button", { name: /previous/i });
  const next = screen.getByRole("button", { name: /next/i });
  expect(prev).toBeDisabled();

  await userEvent.click(next);

  expect(screen.getByLabelText(/slide title/i)).toHaveValue("Two");
  expect(screen.getByTestId("slide-position")).toHaveTextContent("Slide 2 of 3");
  expect(prev).toBeEnabled();
});

test("Next is disabled on the last slide", async () => {
  setup();
  const next = await screen.findByRole("button", { name: /next/i });
  await userEvent.click(next);
  await userEvent.click(next);

  expect(screen.getByLabelText(/slide title/i)).toHaveValue("Three");
  expect(next).toBeDisabled();
});

test("arrow keys change the slide when not typing in a field", async () => {
  setup();
  await screen.findByTestId("slide-position");

  await userEvent.keyboard("{ArrowRight}");
  expect(screen.getByLabelText(/slide title/i)).toHaveValue("Two");

  await userEvent.keyboard("{ArrowLeft}");
  expect(screen.getByLabelText(/slide title/i)).toHaveValue("One");
});

test("arrow keys do not change the slide while typing in a field", async () => {
  setup();
  const title = await screen.findByLabelText(/slide title/i);
  await userEvent.click(title);
  await userEvent.keyboard("{ArrowRight}");

  expect(screen.getByLabelText(/slide title/i)).toHaveValue("One");
});