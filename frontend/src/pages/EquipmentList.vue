<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/api'
import TableList from '@/components/TableList.vue'

const data = ref([])

onMounted(async () => {
  data.value = (await api.get('/equipment')).data
})

const columns = [
  { key: 'id', label: '#' },
  { key: 'name', label: 'Название' },
  { key: 'type', label: 'Тип' },
  { key: 'status', label: 'Статус' },
  { key: 'description', label: 'Описание' },
]
</script>

<template>
  <h2>Оборудование</h2>
  <TableList
    :rows="data"
    :columns="columns"
    :searchable="['name','type','status','description']"
  />
</template>
