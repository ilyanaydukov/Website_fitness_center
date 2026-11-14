import { createPinia } from 'pinia'

// Опционально: можно добавить плагины для Pinia
const pinia = createPinia()

// Пример плагина для сохранения состояния в localStorage
pinia.use(({ store }) => {
  // Восстанавливаем состояние из localStorage
  const savedState = localStorage.getItem(`pinia-${store.$id}`)
  if (savedState) {
    store.$patch(JSON.parse(savedState))
  }

  // Сохраняем состояние при изменении
  store.$subscribe((mutation, state) => {
    localStorage.setItem(`pinia-${store.$id}`, JSON.stringify(state))
  })
})

export default pinia