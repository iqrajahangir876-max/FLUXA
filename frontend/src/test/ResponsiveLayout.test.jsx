import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import App from "../App.jsx";
import { mockApi } from "./mockApi.js";

function setup() {
  mockApi({
    "GET /api/presentations": {
      body: {
        count: 1,
        presentations: [{ id: 1, title: "Deck One", description: "", slide_count: 0 }],
      },
    },
    "GET /api/presentations/1": {
      body: {
        presentation: { id: 1, title: "Deck One", description: "", slide_count: 0, slides: [] },
      },
    },
  });
  render(
    <MemoryRouter initialEntries={["/"]}>
      <App />
    </MemoryRouter>
  );
  return screen.getByRole("complementary", { name: /presentations/i });
}

test("the sidebar is closed by default and the menu button toggles it", async () => {
  const sidebar = setup();
  expect(sidebar).not.toHaveClass("open");

  const toggle = screen.getByRole("button", { name: /toggle sidebar/i });
  await userEvent.click(toggle);
  expect(sidebar).toHaveClass("open");

  await userEvent.click(toggle);
  expect(sidebar).not.toHaveClass("open");
});

test("opening a presentation from the sidebar closes the sidebar", async () => {
  const sidebar = setup();
  await userEvent.click(screen.getByRole("button", { name: /toggle sidebar/i }));
  expect(sidebar).toHaveClass("open");

  await userEvent.click(await within(sidebar).findByRole("link", { name: /Deck One/ }));

  expect(await screen.findByText("No slides yet")).toBeInTheDocument();
  expect(sidebar).not.toHaveClass("open");
});