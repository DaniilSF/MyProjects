<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/api'
import TableList from '@/components/TableList.vue'

const data = ref([])

onMounted(async () => {
  data.value = (await api.get('/locations')).data
})

const columns = [
  { key: 'id', label: '#' },
  { key: 'name', label: 'Название' },
  { key: 'type', label: 'Тип' },
  { key: 'coordinates', label: 'Координаты' },
]
</script>

<template>
  <h2>Места</h2>
  <TableList
    :rows="data"
    :columns="columns"
    :searchable="['name','type','coordinates']"
  />
</template>
