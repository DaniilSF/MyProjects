const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

async function httpJson(url, options = {}) {
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(text || `HTTP ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

export async function apiGetProjects() {
  return httpJson(`${API_BASE}/projects`);
}

export async function apiCreateProject(name) {
  return httpJson(`${API_BASE}/projects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
}

export async function apiDeleteProject(id) {
  return httpJson(`${API_BASE}/projects/${id}`, { method: "DELETE" });
}

export async function apiGetProjectImages(projectId) {
  return httpJson(`${API_BASE}/projects/${projectId}/images`);
}

export async function apiUploadImages(projectId, files) {
  const fd = new FormData();
  for (const f of files) fd.append("files", f);

  const res = await fetch(`${API_BASE}/projects/${projectId}/images`, {
    method: "POST",
    body: fd,
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function apiDeleteImage(imageId) {
  return httpJson(`${API_BASE}/images/${imageId}`, { method: "DELETE" });
}