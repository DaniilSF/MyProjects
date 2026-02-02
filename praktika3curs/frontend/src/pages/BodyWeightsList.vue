<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/api'
import TableList from '@/components/TableList.vue'

const data = ref([])

onMounted(async () => {
  data.value = (await api.get('/body_weights')).data
})

const columns = [
  { key: 'id', label: '#' },
  { key: 'equipment.name', label: 'Оборудование' },
  { key: 'empty_weight_kg', label: 'Пустой, кг' },
  { key: 'max_load_kg', label: 'Г/п, кг' },
  { key: 'effective_date', label: 'Дата' },
]
</script>

<template>
  <h2>Веса кузовов</h2>
  <TableList
    :rows="data"
    :columns="columns"
    :searchable="['equipment.name']"
  />
</template>
