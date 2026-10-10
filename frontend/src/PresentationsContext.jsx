import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { api } from "./api.js";

const PresentationsContext = createContext(null);

export function PresentationsProvider({ children }) {
  const [presentations, setPresentations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const refresh = useCallback(async () => {
    try {
      const data = await api.listPresentations();
      setPresentations(data.presentations);
      setError("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return (
    <PresentationsContext.Provider value={{ presentations, loading, error, refresh }}>
      {children}
    </PresentationsContext.Provider>
  );
}

export const usePresentations = () => useContext(PresentationsContext);
