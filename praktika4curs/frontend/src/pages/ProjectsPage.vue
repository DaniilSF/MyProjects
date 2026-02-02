<script setup>
import { onMounted, ref } from "vue";
import { createProject, deleteProject, getProjects } from "../services/storage.js";

const projects = ref([]);       // реактивный список проектов
const newName = ref("");        // текст из поля ввода
const errorText = ref("");      // текст ошибки (если имя пустое и т.п.)

function refresh() {
  projects.value = getProjects();
}

function onCreate() {
  errorText.value = "";

  try {
    createProject(newName.value);
    newName.value = "";
    refresh();
  } catch (e) {
    errorText.value = "Введите название проекта.";
  }
}

function onDelete(id) {
  // чтобы случайно не удалить проект одним кликом
  const ok = confirm("Удалить проект? Все изображения внутри тоже пропадут.");
  if (!ok) return;

  deleteProject(id);
  refresh();
}

onMounted(() => {
  // Когда страница открылась — загрузим данные из localStorage
  refresh();
});
</script>

<template>
  <div>
    <h1>Projects</h1>

    <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin: 12px 0;">
      <input
        v-model="newName"
        placeholder="Название проекта"
        style="padding: 8px; min-width: 240px;"
        @keydown.enter="onCreate"
      />
      <button style="padding: 8px 12px;" @click="onCreate">Создать</button>
    </div>

    <p v-if="errorText" style="color: #b00020; margin-top: 0;">
      {{ errorText }}
    </p>

    <div v-if="projects.length === 0" style="opacity: 0.8;">
      Пока нет проектов. Создай первый.
    </div>

    <ul v-else style="padding-left: 18px;">
      <li v-for="p in projects" :key="p.id" style="margin: 8px 0;">
        <router-link :to="`/projects/${p.id}`">{{ p.name }}</router-link>
        <span style="opacity: 0.6; margin-left: 8px;">
          ({{ new Date(p.createdAt).toLocaleString() }})
        </span>
        <button style="margin-left: 12px;" @click="onDelete(p.id)">Удалить</button>
      </li>
    </ul>
  </div>
</template>