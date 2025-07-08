<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/api'
import TableList from '@/components/TableList.vue'

const data = ref([])

onMounted(async () => {
  data.value = (await api.get('/shipments')).data
})

const columns = [
  { key: 'id', label: '#' },
  { key: 'planned_datetime', label: 'План' },
  { key: 'status', label: 'Статус' },
  { key: 'equipment.name', label: 'Оборудование' },
  { key: 'cargo_type.name', label: 'Тип груза' },
  { key: 'load_location.name', label: 'Откуда' },
  { key: 'unload_location.name', label: 'Куда' },
  { key: 'weight_kg', label: 'Вес, кг' },
]
</script>

<template>
  <h2>Отгрузки</h2>
  <TableList
    :rows="data"
    :columns="columns"
    :searchable="[
      'equipment.name',
      'cargo_type.name',
      'load_location.name',
      'unload_location.name',
      'status'
    ]"
  />
</template>
