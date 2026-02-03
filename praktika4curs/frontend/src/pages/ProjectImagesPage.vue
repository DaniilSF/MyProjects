<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { apiDeleteImage, apiGetProjectImages, apiUploadImages, apiGetProjects } from "../services/api.js";

const route = useRoute();
const projectId = computed(() => Number(route.params.projectId));

const project = ref(null);
const images = ref([]);
const errorText = ref("");
const isUploading = ref(false);
const isDragging = ref(false);

async function loadProject() {
  // backend не имеет GET /projects/{id}, поэтому берём список и ищем нужный
  const list = await apiGetProjects();
  return list.find((p) => p.id === projectId.value) || null;
}

async function refresh() {
  try {
    errorText.value = "";
    project.value = await loadProject();
    if (!project.value) return;

    images.value = await apiGetProjectImages(projectId.value);
  } catch {
    errorText.value = "Не удалось загрузить проект или изображения";
  }
}

onMounted(refresh);
watch(projectId, refresh);

function onDragOver(e) {
  e.preventDefault();
}

async function onDrop(e) {
  e.preventDefault();
  isDragging.value = false;

  const files = e.dataTransfer?.files;
  if (!files || files.length === 0) return;

  const imageFiles = Array.from(files).filter((f) => f.type?.startsWith("image/"));
  if (imageFiles.length === 0) {
    errorText.value = "Нужны файлы изображений";
    return;
  }

  try {
    errorText.value = "";
    isUploading.value = true;
    await apiUploadImages(projectId.value, imageFiles);
    await refresh();
  } catch {
    errorText.value = "Не удалось добавить изображения.";
  } finally {
    isUploading.value = false;
  }
}

async function onFilesSelected(e) {
  const files = e.target.files;
  if (!files || files.length === 0) return;

  const imageFiles = Array.from(files).filter((f) => f.type?.startsWith("image/"));
  if (imageFiles.length === 0) {
    errorText.value = "Нужны файлы изображений";
    e.target.value = "";
    return;
  }

  try {
    errorText.value = "";
    isUploading.value = true;
    await apiUploadImages(projectId.value, imageFiles);
    e.target.value = "";
    await refresh();
  } catch {
    errorText.value = "Не удалось добавить изображения.";
  } finally {
    isUploading.value = false;
  }
}

async function onDeleteImage(imageId) {
  if (!confirm("Удалить изображение?")) return;
  try {
    await apiDeleteImage(imageId);
    await refresh();
  } catch {
    errorText.value = "Не удалось удалить изображение.";
  }
}
</script>

<template>
  <div>
    <router-link to="/projects">Назад к проектам</router-link>
    <h1>Проект: {{ project?.name ?? "Не найден" }}</h1>
    <p v-if="errorText" class="error">{{ errorText }}</p>
    <div v-if="!project">
      Проект не найден
    </div>
    <div v-else>
      <div
        class="dropzone"
        :class="{ active: isDragging }"
        @dragenter.prevent="isDragging = true"
        @dragover="onDragOver"
        @dragleave="isDragging = false"
        @drop="onDrop"
      >
        <label class="btn">
          {{ isUploading ? "Загрузка..." : "Загрузить" }}
          <input
            class="hidden"
            type="file"
            accept="image/*"
            multiple
            @change="onFilesSelected"
            :disabled="isUploading"
          />
        </label>
        <span>или перетащите изображения сюда</span>
        <span class="count">({{ images.length }})</span>
      </div>
      <div v-if="images.length" class="grid">
        <div v-for="img in images" :key="img.id" class="card">
          <router-link :to="`/projects/${projectId}/images/${img.id}`">
            <img :src="img.url" :alt="img.filename" class="thumb" />
            <div class="filename">{{ img.filename }}</div>
          </router-link>
          <button @click="onDeleteImage(img.id)">Удалить</button>
        </div>
      </div>
      <p v-else>
        Изображений нет
      </p>
    </div>
  </div>
</template>

<style scoped>
.error {
  color: #b00000;
}
.dropzone {
  border: 2px dashed #bbb;
  padding: 12px;
  margin-top: 10px;
}
.dropzone.active {
  background: #ededed;
}
.btn {
  display: inline-block;
  border: 1px solid #ccc;
  padding: 6px 10px;
  cursor: pointer;
  margin-right: 10px;
}
.hidden {
  display: none;
}
.count {
  opacity: 0.8;
  margin-left: 8px;
}
.grid {
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 10px;
}
.card {
  border: 1px solid #ddd;
  padding: 8px;
}
.thumb {
  width: 100%;
  height: 120px;
  object-fit: cover;
  display: block;
}
.filename {
  font-size: 12px;
  margin-top: 6px;
  word-break: break-word;
}
</style>