import { render, screen } from "@testing-library/react";
import SlidePreview from "../components/SlidePreview.jsx";

test("shows the slide counter when slide numbers are given", () => {
  render(<SlidePreview title="Intro" content="Hello" slideNumber={2} totalSlides={5} />);
  expect(screen.getByTestId("preview-count")).toHaveTextContent("2 / 5");
});

test("hides the slide counter when slide numbers are not given", () => {
  render(<SlidePreview title="Intro" content="Hello" />);
  expect(screen.queryByTestId("preview-count")).not.toBeInTheDocument();
});

test("shows a placeholder when the slide has no content", () => {
  render(<SlidePreview title="Intro" content="" />);
  expect(screen.getByText("No content yet")).toBeInTheDocument();
});