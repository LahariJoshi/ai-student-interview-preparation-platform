export function getApiBaseUrl(): string {
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  if (typeof window !== "undefined") {
    const host = window.location.hostname || "localhost";
    return `http://${host}:8000/api/v1`;
  }
  return "http://localhost:8000/api/v1";
}

export async function apiFetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const defaultHeaders: Record<string, string> = {
    "Content-Type": "application/json",
  };

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
    // Crucial: Automatically sends/receives HTTP-Only cookies across requests
    credentials: "include",
  };

  const response = await fetch(`${getApiBaseUrl()}${endpoint}`, config);

  if (!response.ok) {
    let errorMessage = "An unexpected error occurred.";
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorMessage = typeof errorData.detail === "string" ? errorData.detail : JSON.stringify(errorData.detail);
      }
    } catch {
      errorMessage = response.statusText;
    }
    throw new Error(errorMessage);
  }

  return response.json();
}
