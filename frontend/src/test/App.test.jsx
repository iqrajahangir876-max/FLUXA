import { render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import App from "../App.jsx";
import { mockApi } from "./mockApi.js";

const list = {
  body: {
    count: 1,
    presentations: [{ id: 1, title: "Deck One", description: "d", slide_count: 2 }],
  },
};

function renderAt(path) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <App />
    </MemoryRouter>
  );
}

test("renders header, sidebar and the list of presentations", async () => {
  mockApi({ "GET /api/presentations": list });
  renderAt("/");

  expect(screen.getByRole("banner")).toHaveTextContent("FLUXA");

  const sidebar = screen.getByRole("complementary", { name: /presentations/i });
  expect(await within(sidebar).findByRole("link", { name: /Deck One/ })).toBeInTheDocument();
  expect(within(sidebar).getByText("2 slides")).toBeInTheDocument();
});

test("shows an empty state in the sidebar when there are no presentations", async () => {
  mockApi({ "GET /api/presentations": { body: { count: 0, presentations: [] } } });
  renderAt("/");

  expect(await screen.findByText(/no presentations yet/i)).toBeInTheDocument();
});

test("shows a friendly error when the backend is not reachable", async () => {
  vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));
  renderAt("/");

  expect(await screen.findByText(/cannot reach the server/i)).toBeInTheDocument();
});

test("shows a not found page for unknown routes", async () => {
  mockApi({ "GET /api/presentations": list });
  renderAt("/nowhere");

  expect(await screen.findByRole("heading", { name: /page not found/i })).toBeInTheDocument();
});
