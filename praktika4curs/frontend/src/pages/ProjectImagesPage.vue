<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { addImagesToProject, deleteImage, getProjectById } from "../services/storage.js";

const route = useRoute();
const projectId = computed(() => route.params.projectId);

const project = ref(null);
const errorText = ref("");
const isUploading = ref(false);

function refresh() {
  project.value = getProjectById(projectId.value);
}

onMounted(refresh);
watch(projectId, refresh);

const isDragging = ref(false);

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
    await addImagesToProject(projectId.value, imageFiles);
    refresh();
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
    await addImagesToProject(projectId.value, imageFiles);
    e.target.value = "";
    refresh();
  } catch {
    errorText.value = "Не удалось добавить изображения.";
  } finally {
    isUploading.value = false;
  }
}

function onDeleteImage(imageId) {
  if (!confirm("Удалить изображение?")) return;
  deleteImage(projectId.value, imageId);
  refresh();
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
        <span class="count">({{ project.images.length }})</span>
      </div>
      <div v-if="project.images.length" class="grid">
        <div v-for="img in project.images" :key="img.id" class="card">
          <router-link :to="`/projects/${projectId}/images/${img.id}`">
            <img :src="img.dataUrl" :alt="img.filename" class="thumb" />
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