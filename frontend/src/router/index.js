import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/equipment' },
  { path: '/equipment', component: () => import('@/pages/EquipmentList.vue') },
  { path: '/locations', component: () => import('@/pages/LocationsList.vue') },
  { path: '/distances', component: () => import('@/pages/DistancesList.vue') },
  { path: '/body_weights', component: () => import('@/pages/BodyWeightsList.vue') },
  { path: '/cargo_types', component: () => import('@/pages/CargoTypesList.vue') },
  { path: '/shipments', component: () => import('@/pages/ShipmentsList.vue') },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})