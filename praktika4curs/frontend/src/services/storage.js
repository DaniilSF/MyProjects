// src/services/storage.js
const LS_KEY = "pm_projects";

function load() {
  const raw = localStorage.getItem(LS_KEY);
  if (!raw) 
    return [];
  return JSON.parse(raw);
}

function save(projects) {
  localStorage.setItem(LS_KEY, JSON.stringify(projects));
}

function makeId() {
  if (crypto && crypto.randomUUID) 
    return crypto.randomUUID();
  return String(Date.now()) + "_" + String(Math.random()).slice(2);
}

function readFileAsDataURL(file) {
  // позволяет хранить картинку в localStorage
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result));
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}
export function getProjects() {
  return load();
}
export function getProjectById(projectId) {
  const projects = load();
  return projects.find((p) => p.id === projectId) || null;
}
export function createProject(name) {
  const trimmed = String(name ?? "").trim();
  const projects = load();
  const newProject = {
    id: makeId(),
    name: trimmed,
    createdAt: new Date().toISOString(),
    images: [],
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
export async function addImagesToProject(projectId, files) {
  const projects = load();
  const project = projects.find((p) => p.id === projectId);
  const fileList = Array.from(files ?? []);
  for (const file of fileList) {
    const dataUrl = await readFileAsDataURL(file);
    const image = {
      id: makeId(),
      filename: file.name,
      mimeType: file.type,
      size: file.size,
      createdAt: new Date().toISOString(),
      dataUrl,
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
export function getImageById(projectId, imageId) {
  const project = getProjectById(projectId);
  if (!project) return null;
  return project.images.find((img) => img.id === imageId) || null;
}
function annKey(imageId) {
  return `pm_annotations_${imageId}`;
}
export function getAnnotations(imageId) {
  const raw = localStorage.getItem(annKey(imageId));
  if (!raw) return [];
  try {
    return JSON.parse(raw);
  } catch {
    return [];
  }
}
export function saveAnnotations(imageId, annotations) {
  localStorage.setItem(annKey(imageId), JSON.stringify(annotations));
}
