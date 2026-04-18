const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface ApiOptions {
  method?: string;
  body?: unknown;
  token?: string;
}

async function apiRequest(endpoint: string, options: ApiOptions = {}) {
  const { method = "GET", body, token } = options;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || `API error: ${res.status}`);
  }

  // Handle PDF downloads
  if (res.headers.get("content-type")?.includes("application/pdf")) {
    return res.blob();
  }
  return res.json();
}

// Auth
export const authApi = {
  register: (data: { username: string; email: string; password: string; full_name?: string }) =>
    apiRequest("/api/auth/register", { method: "POST", body: data }),
  login: (data: { username: string; password: string }) =>
    apiRequest("/api/auth/login", { method: "POST", body: data }),
  getMe: (token: string) => apiRequest("/api/auth/me", { token }),
};

// Triage
export const triageApi = {
  chat: (data: { message: string; session_id?: string; chat_history?: unknown[]; language?: string }) =>
    apiRequest("/api/triage/chat", { method: "POST", body: data }),
  analyze: (data: { symptoms: string; duration?: string; intensity?: number; medical_history?: string; language?: string }) =>
    apiRequest("/api/triage/analyze", { method: "POST", body: data }),
  getResult: (sessionId: string) => apiRequest(`/api/triage/result/${sessionId}`),
};

// Admin
export const adminApi = {
  getStats: (token?: string) => apiRequest("/api/admin/stats", { token }),
  getCases: (params?: { severity?: string; search?: string; limit?: number; offset?: number }, token?: string) => {
    const query = new URLSearchParams();
    if (params?.severity) query.set("severity", params.severity);
    if (params?.search) query.set("search", params.search);
    if (params?.limit) query.set("limit", String(params.limit));
    if (params?.offset) query.set("offset", String(params.offset));
    return apiRequest(`/api/admin/cases?${query.toString()}`, { token });
  },
  getCase: (sessionId: string, token?: string) =>
    apiRequest(`/api/admin/case/${sessionId}`, { token }),
};

// Reports
export const reportApi = {
  downloadPdf: (sessionId: string) => apiRequest(`/api/reports/${sessionId}/pdf`),
  getData: (sessionId: string) => apiRequest(`/api/reports/${sessionId}/data`),
};

// Translations
export const i18nApi = {
  getTranslations: (lang: string) => apiRequest(`/api/i18n/${lang}`),
  getLanguages: () => apiRequest("/api/i18n/"),
};
