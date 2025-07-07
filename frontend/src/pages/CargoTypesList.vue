<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/api'
import TableList from '@/components/TableList.vue'

const data = ref([])

onMounted(async () => {
  data.value = (await api.get('/cargo_types')).data
})

const columns = [
  { key: 'id', label: '#' },
  { key: 'name', label: 'Название' },
  { key: 'code', label: 'Код' },
  { key: 'density_kg_m3', label: 'Плотность, кг/м³' },
]
</script>

<template>
  <h2>Типы груза</h2>
  <TableList
    :rows="data"
    :columns="columns"
    :searchable="['name','code']"
  />
</template>
