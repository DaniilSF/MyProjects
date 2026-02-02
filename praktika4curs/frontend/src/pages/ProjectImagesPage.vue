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

// если пользователь сменит URL на другой projectId — обновим страницу
watch(projectId, refresh);

async function onFilesSelected(e) {
  errorText.value = "";
  const files = e.target.files;

  if (!files || files.length === 0) return;

  try {
    isUploading.value = true;
    await addImagesToProject(projectId.value, files);
    e.target.value = ""; // чтобы можно было выбрать те же файлы ещё раз
    refresh();            // <-- главное: обновили UI сразу
  } catch (err) {
    errorText.value = "Не удалось добавить изображения.";
  } finally {
    isUploading.value = false;
  }
}

function onDeleteImage(imageId) {
  const ok = confirm("Удалить изображение?");
  if (!ok) return;

  deleteImage(projectId.value, imageId);
  refresh(); // <-- UI обновится сразу, без F5
}
</script>

<template>
  <div>
    <router-link to="/projects">← Назад к проектам</router-link>

    <h1 style="margin-top: 12px">
      Проект: {{ project?.name ?? "Не найден" }}
    </h1>

    <p v-if="errorText" style="color: #b00020">{{ errorText }}</p>

    <div v-if="!project" style="margin-top: 16px">
      Проект не найден. Проверь URL.
    </div>

    <div v-else style="margin-top: 16px">
      <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
        <label
          style="display: inline-block; padding: 8px 12px; border: 1px solid #ccc; cursor: pointer;"
        >
          {{ isUploading ? "Загрузка..." : "Загрузить изображения" }}
          <input
            type="file"
            accept="image/*"
            multiple
            style="display: none"
            @change="onFilesSelected"
            :disabled="isUploading"
          />
        </label>

        <span style="opacity: 0.75">
          Всего изображений: {{ project.images.length }}
        </span>
      </div>

      <div
        v-if="project.images.length"
        style="
          margin-top: 16px;
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
          gap: 12px;
        "
      >
        <div
          v-for="img in project.images"
          :key="img.id"
          style="border: 1px solid #ddd; padding: 8px;"
        >
          <router-link
            :to="`/projects/${projectId}/images/${img.id}`"
            style="text-decoration: none; color: inherit;"
          >
            <img
              :src="img.dataUrl"
              :alt="img.filename"
              style="width: 100%; height: 120px; object-fit: cover; display: block;"
            />
            <div style="margin-top: 6px; font-size: 12px; word-break: break-word;">
              {{ img.filename }}
            </div>
          </router-link>

          <button style="margin-top: 8px; width: 100%;" @click="onDeleteImage(img.id)">
            Удалить
          </button>
        </div>
      </div>

      <p v-else style="margin-top: 16px; opacity: 0.8">
        В проекте пока нет изображений. Нажми “Загрузить изображения”.
      </p>
    </div>
  </div>
</template>