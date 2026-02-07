<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { apiGetProjectImages, apiGetAnnotations, apiSaveAnnotations, apiPredict } from "../services/api.js";

const route = useRoute();
const projectId = computed(() => Number(route.params.projectId));
const imageId = computed(() => Number(route.params.imageId));

const image = ref(null);
const errorText = ref("");

const boxes = ref([]); // фронтовый вид: { id?, x,y,w,h, className }

const isDrawing = ref(false);
const start = ref({ x: 0, y: 0 });
const current = ref({ x: 0, y: 0 });

const hoverBoxId = ref(null);
const hoverPos = ref({ x: 0, y: 0 });

const imgWrap = ref(null);

const formVisible = ref(false);
const formMode = ref("create"); // create | edit
const formClass = ref("");
const editBoxId = ref(null);
const pendingRect = ref(null);

const isSaving = ref(false);
const isPredicting = ref(false);

// ----- ZOOM -----
const zoom = ref(1); // 1..3

const classOptions = computed(() => {
  const set = new Set();
  for (const b of boxes.value) if (b.className) set.add(b.className);
  return Array.from(set).sort();
});

function clamp01(v) {
  return Math.max(0, Math.min(1, v));
}

function getRelativePoint(e) {
  const rect = imgWrap.value.getBoundingClientRect();

  const xScaled = e.clientX - rect.left;
  const yScaled = e.clientY - rect.top;

  const w0 = rect.width / zoom.value;
  const h0 = rect.height / zoom.value;

  const x01 = clamp01((xScaled / zoom.value) / w0);
  const y01 = clamp01((yScaled / zoom.value) / h0);

  return { x: x01, y: y01 };
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

function boxStyle(b) {
  return {
    left: (b.x * 100).toFixed(3) + "%",
    top: (b.y * 100).toFixed(3) + "%",
    width: (b.w * 100).toFixed(3) + "%",
    height: (b.h * 100).toFixed(3) + "%",
  };
}

function formatBoxInfo(b) {
  return b ? b.className : "";
}

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

async function reloadAnnotations() {
  try {
    const list = await apiGetAnnotations(imageId.value);
    boxes.value = (list ?? []).map((a) => ({
      id: a.id,
      x: a.x,
      y: a.y,
      w: a.w,
      h: a.h,
      className: a.class_name,
    }));
  } catch {
    errorText.value = "Не удалось загрузить аннотации";
  }
}

async function persistBoxes() {
  try {
    isSaving.value = true;
    await apiSaveAnnotations(imageId.value, boxes.value);
    await reloadAnnotations();
  } catch {
    errorText.value = "Не удалось сохранить аннотации";
  } finally {
    isSaving.value = false;
  }
}

async function saveForm() {
  const cls = String(formClass.value ?? "").trim();
  if (!cls) return;

  if (formMode.value === "create") {
    if (!pendingRect.value) return;

    const rect = pendingRect.value;
    const newBox = {
      x: rect.left,
      y: rect.top,
      w: rect.w,
      h: rect.h,
      className: cls,
    };

    boxes.value = [newBox, ...boxes.value];
    closeForm();
    await persistBoxes();
    return;
  }

  if (formMode.value === "edit") {
    const id = editBoxId.value;
    if (!id) return;

    const b = boxes.value.find((x) => x.id === id);
    if (!b) return;

    b.className = cls;
    boxes.value = [...boxes.value];
    closeForm();
    await persistBoxes();
  }
}

async function deleteEditedBox() {
  const id = editBoxId.value;
  if (!id) return;

  boxes.value = boxes.value.filter((x) => x.id !== id);
  closeForm();
  await persistBoxes();
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
  const xScaled = e.clientX - rect.left;
  const yScaled = e.clientY - rect.top;

  hoverPos.value = {
    x: xScaled / zoom.value,
    y: yScaled / zoom.value,
  };

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

function onBoxClick(b) {
  openEditForm(b);
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

async function loadAll() {
  await loadImageFromApi();
  if (image.value) await reloadAnnotations();
}

onMounted(loadAll);
watch([projectId, imageId], loadAll);

async function onPredictClick() {
  if (!image.value) return;

  try {
    errorText.value = "";
    isPredicting.value = true;
    await apiPredict(imageId.value);
    await reloadAnnotations();
  } catch {
    errorText.value = "Не удалось выполнить ML predict";
  } finally {
    isPredicting.value = false;
  }
}
</script>

<template>
  <div>
    <router-link :to="`/projects/${projectId}`">Назад к проекту</router-link>

    <div v-if="errorText" class="error">
      {{ errorText }}
    </div>

    <div v-if="image" class="page">
      <!-- Левая колонка: картинка -->
      <div class="left">
        <h2 class="title">
          {{ image.filename }}
          <span v-if="isSaving" class="muted">(сохраняю...)</span>
        </h2>

        <div class="img-frame">
          <div
            ref="imgWrap"
            class="img-wrap"
            :style="{ transform: `scale(${zoom})` }"
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
              :key="b.id ?? `${b.x}_${b.y}_${b.w}_${b.h}_${b.className}`"
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
          </div>
        </div>
      </div>

      <!-- Правая колонка: управление -->
      <div class="right">
        <div class="panel">
          <div class="panel-row">
            <div class="panel-title">Управление</div>
          </div>

          <label class="zoom">
            Zoom: {{ zoom.toFixed(1) }}x
            <input type="range" min="1" max="3" step="0.1" v-model.number="zoom" />
          </label>

          <button class="btn" @click="onPredictClick" :disabled="isPredicting || isSaving || formVisible">
            {{ isPredicting ? "ML..." : "ML Predict" }}
          </button>
        </div>

        <!-- Форма теперь ЗДЕСЬ, вне картинки -->
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

        <div v-else class="panel-hint">
          ЛКМ: рисовать прямоугольник. Клик по боксу для: изменить класс / удалить.
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.error {
  margin-top: 12px;
  color: #b00000;
}

.page {
  margin-top: 12px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 280px;
  gap: 16px;
  align-items: start;
}

@media (max-width: 900px) {
  .page {
    grid-template-columns: 1fr;
  }
  .right {
    order: 2;
  }
}

.title {
  margin: 0 0 8px 0;
}

.muted {
  font-size: 12px;
  opacity: 0.7;
  margin-left: 8px;
}

.img-frame {
  border: 1px solid #ddd;
  overflow: auto;
  max-width: 900px;
  width: 100%;
}

.img-wrap {
  position: relative;
  width: 100%;
  transform-origin: top left;
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

.hint {
  margin-top: 10px;
  opacity: 0.8;
}

/* Правая панель */
.panel {
  border: 1px solid #ddd;
  padding: 10px;
}

.panel-title {
  font-weight: 600;
  margin-bottom: 8px;
}

.zoom {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 12px;
  margin-bottom: 10px;
}

.btn {
  padding: 6px 10px;
}

.class-form {
  margin-top: 12px;
  border: 1px solid #ddd;
  padding: 10px;
  font-size: 12px;
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

.panel-hint {
  margin-top: 12px;
  font-size: 12px;
  opacity: 0.75;
}
</style>