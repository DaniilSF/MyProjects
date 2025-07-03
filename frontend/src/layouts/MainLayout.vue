<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Dispatcher</a>
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li v-for="l in links" :key="l.to" class="nav-item">
            <RouterLink class="nav-link" :to="l.to" active-class="active">{{ l.label }}</RouterLink>
          </li>
        </ul>
      </div>
    </nav>

    <main class="container py-3">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
const links = [
  { to: '/equipment',    label: 'Оборудование' },
  { to: '/locations',    label: 'Места' },
  { to: '/distances',    label: 'Расстояния' },
  { to: '/body_weights', label: 'Веса кузовов' },
  { to: '/cargo_types',  label: 'Типы груза' },
  { to: '/shipments',    label: 'Отгрузки' },
]
</script>
