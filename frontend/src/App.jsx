import { Routes, Route, Link } from "react-router-dom";
import { PresentationsProvider } from "./PresentationsContext.jsx";
import Layout from "./components/Layout.jsx";
import Home from "./pages/Home.jsx";
import CreatePresentation from "./pages/CreatePresentation.jsx";
import EditorPage from "./pages/EditorPage.jsx";

function NotFound() {
  return (
    <div className="empty">
      <h1>Page not found</h1>
      <p className="muted">The page you are looking for does not exist.</p>
      <Link to="/" className="btn">Back to home</Link>
    </div>
  );
}

export default function App() {
  return (
    <PresentationsProvider>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="create" element={<CreatePresentation />} />
          <Route path="presentations/:id" element={<EditorPage />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </PresentationsProvider>
  );
}
