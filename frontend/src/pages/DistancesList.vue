<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/api'
import TableList from '@/components/TableList.vue'

const data = ref([])

onMounted(async () => {
  data.value = (await api.get('/distances')).data
})

const columns = [
  { key: 'id', label: '#' },
  { key: 'from_location.name', label: 'Откуда' },
  { key: 'to_location.name', label: 'Куда' },
  { key: 'distance_km', label: 'Расстояние, км' },
  { key: 'estimated_time_min', label: 'Время, мин' },
]
</script>

<template>
  <h2>Расстояния</h2>
  <TableList
    :rows="data"
    :columns="columns"
    :searchable="['from_location.name','to_location.name']"
  />
</template>
