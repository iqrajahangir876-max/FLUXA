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
      body: { count: 1, presentations: [{ id: 3, title: "Deck", description: "", slide_count: 2 }] },
    },
    "GET /api/presentations/3": {
      body: {
        presentation: {
          id: 3,
          title: "Deck",
          description: "",
          slide_count: 2,
          slides: [slide(10, 1, "One", "a"), slide(11, 2, "Two", "b")],
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

beforeEach(() => {
  localStorage.clear();
});

test("uses the Midnight theme and Standard layout by default", async () => {
  setup();
  const preview = await screen.findByTestId("slide-preview");
  expect(preview).toHaveClass("theme-midnight");
  expect(preview).toHaveClass("layout-standard");
});

test("changing the theme updates the preview", async () => {
  setup();
  await userEvent.selectOptions(await screen.findByLabelText("Theme"), "ocean");
  expect(screen.getByTestId("slide-preview")).toHaveClass("theme-ocean");
});

test("changing the layout updates the preview", async () => {
  setup();
  await userEvent.selectOptions(await screen.findByLabelText("Layout"), "centered");
  expect(screen.getByTestId("slide-preview")).toHaveClass("layout-centered");
});

test("the theme is remembered after reopening the editor", async () => {
  const first = setup();
  await userEvent.selectOptions(await screen.findByLabelText("Theme"), "sunset");
  first.unmount();

  setup();
  const preview = await screen.findByTestId("slide-preview");
  expect(preview).toHaveClass("theme-sunset");
});

test("the layout belongs to one slide only", async () => {
  setup();
  await userEvent.selectOptions(await screen.findByLabelText("Layout"), "two-column");
  expect(screen.getByTestId("slide-preview")).toHaveClass("layout-two-column");

  await userEvent.click(screen.getByRole("button", { name: /next/i }));

  expect(screen.getByLabelText(/slide title/i)).toHaveValue("Two");
  expect(screen.getByTestId("slide-preview")).toHaveClass("layout-standard");
  expect(screen.getByTestId("slide-preview")).toHaveClass("theme-midnight");
});