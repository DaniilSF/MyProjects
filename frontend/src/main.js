import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'   // стиль Bootstrap 5

createApp(App)
  .use(router)
  .use(createPinia())
  .mount('#app')
