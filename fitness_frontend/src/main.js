import { createApp } from 'vue'
import pinia from './store'
import App from './App.vue'
import router from './router'
import './assets/styles/main.css'

// Импортируем и инициализируем сторы
import { useAuthStore } from './store/auth'

const app = createApp(App)

// Используем Pinia и Router
app.use(pinia)
app.use(router)

// Инициализируем аутентификацию при старте приложения
const authStore = useAuthStore()
authStore.initAuth()

// Попытка загрузить пользователя если есть токен
if (authStore.token) {
  authStore.fetchUser()
}

app.mount('#app')