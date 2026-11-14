import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  const isLoading = ref(false)
  const loadingMessage = ref('')
  const notifications = ref([])
  const sidebarOpen = ref(true)
  const theme = ref('dark')

  const showLoading = (message = '') => {
    isLoading.value = true
    loadingMessage.value = message
  }

  const hideLoading = () => {
    isLoading.value = false
    loadingMessage.value = ''
  }

  const addNotification = (notification) => {
    notifications.value.push({
      id: Date.now(),
      ...notification
    })
    
    // Автоматическое удаление уведомлений через 5 секунд
    setTimeout(() => {
      notifications.value = notifications.value.filter(n => n.id !== notification.id)
    }, 5000)
  }

  const removeNotification = (id) => {
    notifications.value = notifications.value.filter(notification => notification.id !== id)
  }

  const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value
  }

  const toggleTheme = () => {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
  }

  return {
    isLoading,
    loadingMessage,
    notifications,
    sidebarOpen,
    theme,
    showLoading,
    hideLoading,
    addNotification,
    removeNotification,
    toggleSidebar,
    toggleTheme
  }
})