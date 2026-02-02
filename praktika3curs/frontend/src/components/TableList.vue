<template>
  <div>
    <!-- поле поиска -->
    <input
      v-model="search"
      class="form-control mb-2"
      placeholder="Поиск…"
    />

    <!-- табличка -->
    <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th v-for="c in columns" :key="c.key">{{ c.label }}</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="r in filtered" :key="r.id">
          <!-- lodash/get позволяет писать 'equipment.name' и т.д. -->
          <td v-for="c in columns" :key="c.key">
            {{ get(r, c.key) }}
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="!rows.length" class="text-muted">Данных пока нет…</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import get from 'lodash/get'      // уже есть после   npm install

const props = defineProps({
  rows:       { type: Array, default: () => [] },
  columns:    { type: Array, required: true },   // [{key,label}, …]
  searchable: { type: Array, default: () => [] } // ['name','type']
})

const search = ref('')

const filtered = computed(() => {
  if (!search.value) return props.rows
  const q = search.value.toLowerCase()

  return props.rows.filter(row =>
    props.searchable.some(field => {
      const v = String(get(row, field) ?? '').toLowerCase()
      return v.includes(q)
    })
  )
})
</script>
