<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { apiGetProjectImages } from "../services/api.js";
import { getAnnotations, saveAnnotations } from "../services/storage.js";

const route = useRoute();
const projectId = computed(() => Number(route.params.projectId));
const imageId = computed(() => Number(route.params.imageId));

const image = ref(null);
const errorText = ref("");

const boxes = ref([]);

const isDrawing = ref(false);
const start = ref({ x: 0, y: 0 });
const current = ref({ x: 0, y: 0 });

const hoverBoxId = ref(null);
const hoverPos = ref({ x: 0, y: 0 });

const imgWrap = ref(null);
const formVisible = ref(false);
const formMode = ref("create");
const formClass = ref("");
const editBoxId = ref(null);
const pendingRect = ref(null);

const classOptions = computed(() => {
  const set = new Set();
  for (const b of boxes.value) if (b.className) set.add(b.className);
  return Array.from(set).sort();
});

function makeId() {
  if (crypto && crypto.randomUUID) return crypto.randomUUID();
  return String(Date.now()) + "_" + String(Math.random()).slice(2);
}
function clamp01(v) {
  return Math.max(0, Math.min(1, v));
}
function getRelativePoint(e) {
  const rect = imgWrap.value.getBoundingClientRect();
  const x = clamp01((e.clientX - rect.left) / rect.width);
  const y = clamp01((e.clientY - rect.top) / rect.height);
  return { x, y };
}

const previewBox = computed(() => {
  if (!isDrawing.value) return null;

  const x1 = start.value.x;
  const y1 = start.value.y;
  const x2 = current.value.x;
  const y2 = current.value.y;

  const left = Math.min(x1, x2);
  const top = Math.min(y1, y2);
  const w = Math.abs(x2 - x1);
  const h = Math.abs(y2 - y1);

  if (w < 0.005 || h < 0.005) return null;
  return { left, top, w, h };
});

function openCreateForm(rect) {
  formMode.value = "create";
  formVisible.value = true;
  pendingRect.value = rect;
  editBoxId.value = null;
  formClass.value = classOptions.value[0] ?? "object";
  hoverBoxId.value = null;
}
function openEditForm(box) {
  formMode.value = "edit";
  formVisible.value = true;
  editBoxId.value = box.id;
  pendingRect.value = null;
  formClass.value = box.className ?? "";
  hoverBoxId.value = null;
}
function closeForm() {
  formVisible.value = false;
  pendingRect.value = null;
  editBoxId.value = null;
  formClass.value = "";
}

function saveForm() {
  const cls = String(formClass.value ?? "").trim();
  if (!cls) return;

  if (formMode.value === "create") {
    if (!pendingRect.value) return;

    const rect = pendingRect.value;
    const newBox = {
      id: makeId(),
      x: rect.left,
      y: rect.top,
      w: rect.w,
      h: rect.h,
      className: cls,
    };

    boxes.value = [newBox, ...boxes.value];
    saveAnnotations(imageId.value, boxes.value);
    closeForm();
    return;
  }

  if (formMode.value === "edit") {
    const id = editBoxId.value;
    if (!id) return;

    const b = boxes.value.find((x) => x.id === id);
    if (!b) return;

    b.className = cls;
    boxes.value = [...boxes.value];
    saveAnnotations(imageId.value, boxes.value);
    closeForm();
  }
}

function deleteEditedBox() {
  const id = editBoxId.value;
  if (!id) return;
  boxes.value = boxes.value.filter((x) => x.id !== id);
  saveAnnotations(imageId.value, boxes.value);
  closeForm();
}

function onMouseDown(e) {
  if (e.button !== 0) return;
  if (!imgWrap.value) return;
  if (formVisible.value) return;

  e.preventDefault();
  isDrawing.value = true;

  const p = getRelativePoint(e);
  start.value = p;
  current.value = p;
}
function onMouseMove(e) {
  if (!imgWrap.value) return;

  const rect = imgWrap.value.getBoundingClientRect();
  hoverPos.value = { x: e.clientX - rect.left, y: e.clientY - rect.top };

  if (!isDrawing.value) return;
  current.value = getRelativePoint(e);
}

function finishDrawing() {
  const pb = previewBox.value;
  isDrawing.value = false;
  if (!pb) return;
  openCreateForm(pb);
}

function onMouseUp(e) {
  if (e.button !== 0) return;
  if (!isDrawing.value) return;
  finishDrawing();
}
function onMouseLeave() {
  if (isDrawing.value) finishDrawing();
  hoverBoxId.value = null;
}

function boxStyle(b) {
  return {
    left: (b.x * 100).toFixed(3) + "%",
    top: (b.y * 100).toFixed(3) + "%",
    width: (b.w * 100).toFixed(3) + "%",
    height: (b.h * 100).toFixed(3) + "%",
  };
}
function onBoxClick(b) {
  openEditForm(b);
}
function formatBoxInfo(b) {
  return b ? b.className : "";
}

async function loadImageFromApi() {
  try {
    errorText.value = "";
    const list = await apiGetProjectImages(projectId.value);
    image.value = list.find((x) => x.id === imageId.value) || null;
    if (!image.value) errorText.value = "Изображение не найдено";
  } catch {
    errorText.value = "Не удалось загрузить изображение";
    image.value = null;
  }
}

function loadAnnotations() {
  boxes.value = getAnnotations(imageId.value);
}
onMounted(async () => {
  await loadImageFromApi();
  loadAnnotations();
});
watch([projectId, imageId], async () => {
  await loadImageFromApi();
  loadAnnotations();
});
</script>

<template>
  <div>
    <router-link :to="`/projects/${projectId}`">Назад к проекту</router-link>

    <div v-if="errorText" style="margin-top: 12px; color:#b00000;">
      {{ errorText }}
    </div>

    <div v-if="image" style="margin-top: 12px;">
      <h2 style="margin: 0 0 8px 0;">{{ image.filename }}</h2>

      <div
        ref="imgWrap"
        class="img-wrap"
        @mousedown="onMouseDown"
        @mousemove="onMouseMove"
        @mouseup="onMouseUp"
        @mouseleave="onMouseLeave"
      >
        <img
          :src="image.url"
          :alt="image.filename"
          class="img"
          draggable="false"
          @dragstart.prevent
        />

        <div
          v-for="b in boxes"
          :key="b.id"
          class="box"
          :style="boxStyle(b)"
          @mouseenter="hoverBoxId = b.id"
          @mouseleave="hoverBoxId = null"
          @click.stop="onBoxClick(b)"
        ></div>

        <div
          v-if="previewBox"
          class="box preview"
          :style="{
            left: (previewBox.left * 100) + '%',
            top: (previewBox.top * 100) + '%',
            width: (previewBox.w * 100) + '%',
            height: (previewBox.h * 100) + '%'
          }"
        ></div>

        <div
          v-if="hoverBoxId && !formVisible"
          class="tooltip"
          :style="{ left: hoverPos.x + 12 + 'px', top: hoverPos.y + 12 + 'px' }"
        >
          {{ formatBoxInfo(boxes.find(x => x.id === hoverBoxId)) }}
        </div>

        <div v-if="formVisible" class="class-form" @mousedown.stop @click.stop>
          <div class="form-title">
            {{ formMode === "create" ? "Новый бокс" : "Редактирование бокса" }}
          </div>

          <input
            v-model="formClass"
            class="form-input"
            list="classList"
            placeholder="Класс"
            @keydown.enter.prevent="saveForm"
          />

          <datalist id="classList">
            <option v-for="c in classOptions" :key="c" :value="c"></option>
          </datalist>

          <div class="form-actions">
            <button @click="saveForm">Сохранить</button>
            <button @click="closeForm">Отмена</button>
            <button v-if="formMode === 'edit'" @click="deleteEditedBox">Удалить</button>
          </div>
        </div>
      </div>

      <p class="hint">
        ЛКМ: рисовать прямоугольник. Клик по боксу: изменить класс / удалить.
      </p>
    </div>
  </div>
</template>

<style scoped>
.img-wrap {
  position: relative;
  max-width: 900px;
  width: 100%;
  border: 1px solid #ddd;
  user-select: none;
}
.img {
  width: 100%;
  height: auto;
  display: block;
}
.box {
  position: absolute;
  border: 2px solid #00a000;
  box-sizing: border-box;
  cursor: pointer;
}
.box.preview {
  border-style: dashed;
  cursor: default;
}
.tooltip {
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  padding: 6px 8px;
  font-size: 12px;
  pointer-events: none;
  white-space: nowrap;
}
.class-form {
  position: absolute;
  left: 12px;
  top: 12px;
  background: white;
  border: 1px solid #ccc;
  padding: 10px;
  font-size: 12px;
  width: 260px;
}
.form-title {
  font-weight: 600;
  margin-bottom: 8px;
}
.form-input {
  width: 100%;
  box-sizing: border-box;
  padding: 6px 8px;
  margin-bottom: 8px;
}
.form-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.hint {
  margin-top: 10px;
  opacity: 0.8;
}
</style>