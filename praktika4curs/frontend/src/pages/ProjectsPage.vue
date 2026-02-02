<script setup>
import { onMounted, ref } from "vue";
import { createProject, deleteProject, getProjects } from "../services/storage.js";

const projects = ref([]);
const newName = ref("");
const errorText = ref("");

function refresh() {
  projects.value = getProjects();
}

function onCreate() {
  const name = newName.value.trim();
  if (!name) {
    errorText.value = "Введите название проекта";
    return;
  }
  try {
    errorText.value = "";
    createProject(name);
    newName.value = "";
    refresh();
  } catch {
    errorText.value = "Не удалось создать проект";
  }
}

function onDelete(id) {
  if (!confirm("Удалить проект? Все изображения пропадут")) return;
  deleteProject(id);
  refresh();
}

onMounted(refresh);
</script>

<template>
  <div>
    <h1>Projects</h1>
    <div class="row">
      <input
        v-model="newName"
        class="input"
        placeholder="Название проекта"
        @keydown.enter="onCreate"
      />
      <button class="btn" @click="onCreate">Создать</button>
    </div>
    <p v-if="errorText" class="error">{{ errorText }}</p>
    <div v-if="projects.length === 0" class="hint">
      Проектов нет
    </div>
    <ul v-else class="list">
      <li v-for="p in projects" :key="p.id" class="item">
        <router-link :to="`/projects/${p.id}`">
          {{ p.name }}
        </router-link>
        <span>
          ({{ new Date(p.createdAt).toLocaleString() }})
        </span>
        <button @click="onDelete(p.id)">Удалить</button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.row {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  margin: 12px 0;
}
.input {
  padding: 8px;
  min-width: 240px;
}
.btn {
  padding: 8px 12px;
}
.error {
  color: #b00000;
  margin-top: 0;
}
.hint {
  opacity: 0.8;
}
.list {
  padding-left: 18px;
}
.item {
  margin: 8px 0;
}
</style>