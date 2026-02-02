// src/services/storage.js

const LS_KEY = "pm_projects_v1"; // ключ в localStorage

function load() {
  // localStorage хранит только строки, поэтому читаем JSON-строку и парсим.
  const raw = localStorage.getItem(LS_KEY);
  if (!raw) return [];
  try {
    return JSON.parse(raw);
  } catch (e) {
    // если вдруг данные в localStorage "сломались", безопасно вернём пусто
    return [];
  }
}

function save(projects) {
  localStorage.setItem(LS_KEY, JSON.stringify(projects));
}

function makeId() {
  // На тестовое достаточно простого id.
  // crypto.randomUUID() поддерживается в современных браузерах.
  if (crypto && crypto.randomUUID) return crypto.randomUUID();
  return String(Date.now()) + "_" + String(Math.random()).slice(2);
}

function readFileAsDataURL(file) {
  // Превращает файл в строку вида "data:image/png;base64,...."
  // Это позволяет хранить картинку в localStorage и показывать её после F5.
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result));
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

// --- API нашего "хранилища" ---

export function getProjects() {
  return load();
}

export function getProjectById(projectId) {
  const projects = load();
  return projects.find((p) => p.id === projectId) || null;
}

export function createProject(name) {
  const trimmed = String(name ?? "").trim();
  if (!trimmed) {
    throw new Error("Project name is empty");
  }

  const projects = load();

  const newProject = {
    id: makeId(),
    name: trimmed,
    createdAt: new Date().toISOString(),
    images: [], // здесь будут изображения (dataUrl + метаданные)
  };

  projects.unshift(newProject);
  save(projects);

  return newProject;
}

export function deleteProject(projectId) {
  const projects = load();
  const next = projects.filter((p) => p.id !== projectId);
  save(next);
}

// ВАЖНО: функция async, потому что FileReader работает асинхронно
export async function addImagesToProject(projectId, files) {
  const projects = load();
  const project = projects.find((p) => p.id === projectId);
  if (!project) throw new Error("Project not found");

  const fileList = Array.from(files ?? []);
  for (const file of fileList) {
    const dataUrl = await readFileAsDataURL(file);

    const image = {
      id: makeId(),
      filename: file.name,
      mimeType: file.type,
      size: file.size,
      createdAt: new Date().toISOString(),
      dataUrl, // <-- вместо blob: url
    };

    project.images.unshift(image);
  }

  save(projects);
}

export function deleteImage(projectId, imageId) {
  const projects = load();
  const project = projects.find((p) => p.id === projectId);
  if (!project) return;

  project.images = project.images.filter((x) => x.id !== imageId);
  save(projects);
}