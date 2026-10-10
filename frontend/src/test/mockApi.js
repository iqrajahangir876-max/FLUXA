import { vi } from "vitest";

// handlers: { "METHOD /api/path": { status?, body } | (call) => { status?, body } }
export function mockApi(handlers) {
  const calls = [];

  vi.stubGlobal(
    "fetch",
    vi.fn(async (url, options = {}) => {
      const method = (options.method || "GET").toUpperCase();
      const call = {
        method,
        url,
        body: options.body ? JSON.parse(options.body) : null,
      };
      calls.push(call);

      const handler = handlers[`${method} ${url}`];
      const result = handler
        ? typeof handler === "function" ? handler(call) : handler
        : { status: 404, body: { error: `Not mocked: ${method} ${url}` } };

      const status = result.status || 200;
      return { ok: status < 400, status, json: async () => result.body };
    })
  );

  return calls;
}
