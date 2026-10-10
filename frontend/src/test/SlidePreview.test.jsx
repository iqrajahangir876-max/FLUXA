import { render, screen } from "@testing-library/react";
import SlidePreview from "../components/SlidePreview.jsx";

test("renders the title and content lines", () => {
  render(<SlidePreview title="Intro" content={"Welcome\n- First point\n- Second point"} />);

  expect(screen.getByRole("heading", { name: "Intro" })).toBeInTheDocument();
  expect(screen.getByText("Welcome")).not.toHaveClass("bullet");
  expect(screen.getByText("First point")).toHaveClass("bullet");
  expect(screen.getByText("Second point")).toHaveClass("bullet");
});

test("falls back to a placeholder title", () => {
  render(<SlidePreview title="" content="" />);

  expect(screen.getByRole("heading", { name: "Untitled slide" })).toBeInTheDocument();
});
