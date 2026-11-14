<!-- ServiceManagement.vue -->
<template>
  <div class="container">
    <div class="admin-header">
      <h1 class="page-title">Управление услугами</h1>
      <button @click="showCreateModal = true" class="btn btn-primary">
        + Добавить услугу
      </button>
    </div>
    
    <div v-if="isLoading" class="loader"></div>
    
    <div v-else>
      <div class="search-filter">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Поиск по названию или описанию..."
          class="form-control"
          @input="debouncedSearch"
        />
      </div>
      
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Описание</th>
            <th>Цена (₽)</th>
            <th>Длительность (мин)</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in filteredServices" :key="service.id">
            <td>{{ service.id }}</td>
            <td>
              <strong>{{ service.name }}</strong>
            </td>
            <td>
              <div class="description-truncate">
                {{ service.description || 'Нет описания' }}
              </div>
            </td>
            <td>{{ service.price ? service.price.toFixed(2) : '0.00' }}</td>
            <td>{{ service.duration || '60' }}</td>
            <td>
              <button @click="editService(service)" class="btn btn-sm btn-secondary me-2">
                Редактировать
              </button>
              <button @click="deleteService(service.id)" class="btn btn-sm btn-danger">
                Удалить
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="filteredServices.length === 0" class="empty-state">
        <p>{{ searchQuery ? 'Услуги не найдены по запросу' : 'Услуги не найдены' }}</p>
        <button @click="showCreateModal = true" class="btn btn-primary">
          Создать первую услугу
        </button>
      </div>
    </div>
    
    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editingService ? 'Редактировать' : 'Добавить' }} услугу</h3>
          <button @click="closeModal" class="btn btn-sm btn-danger">&times;</button>
        </div>
        
        <form @submit.prevent="saveService" class="modal-form">
          <div class="form-group mb-3">
            <label class="form-label">Название *</label>
            <input 
              type="text" 
              v-model="serviceForm.name" 
              required 
              class="form-control" 
              placeholder="Например: Йога для начинающих"
            />
          </div>
          
          <div class="form-group mb-3">
            <label class="form-label">Описание</label>
            <textarea 
              v-model="serviceForm.description" 
              class="form-control" 
              rows="4"
              placeholder="Подробное описание услуги, что входит в занятие..."
              maxlength="500"
            ></textarea>
            <div class="char-count text-end mt-1">
              {{ serviceForm.description?.length || 0 }}/500 символов
            </div>
          </div>
          
          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Цена (₽)</label>
              <input 
                type="number" 
                v-model="serviceForm.price" 
                class="form-control" 
                min="0" 
                step="0.01"
                placeholder="0.00"
              />
              <small class="form-text text-muted">0.00 - если услуга бесплатная</small>
            </div>
            <div class="col-md-6">
              <label class="form-label">Длительность (мин)</label>
              <input 
                type="number" 
                v-model="serviceForm.duration" 
                class="form-control" 
                min="1"
                placeholder="60"
              />
              <small class="form-text text-muted">Длительность одного занятия в минутах</small>
            </div>
          </div>
          
          <div v-if="errorMessage" class="alert alert-danger mb-3">
            {{ errorMessage }}
          </div>
          
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary" :disabled="isSaving">
              {{ isSaving ? 'Сохранение...' : 'Сохранить' }}
            </button>
            <button type="button" @click="closeModal" class="btn btn-secondary">
              Отмена
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { fitnessAPI } from '../../services/api'

export default {
  name: 'ServiceManagement',
  setup() {
    const services = ref([])
    const isLoading = ref(false)
    const isSaving = ref(false)
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const editingService = ref(null)
    const searchQuery = ref('')
    const errorMessage = ref('')
    let searchTimeout = null
    
    const serviceForm = ref({
      name: '',
      description: '',
      price: '',
      duration: ''
    })
    
    const filteredServices = computed(() => {
      if (!searchQuery.value.trim()) return services.value
      
      const query = searchQuery.value.toLowerCase().trim()
      return services.value.filter(service => 
        service.name?.toLowerCase().includes(query) ||
        service.description?.toLowerCase().includes(query)
      )
    })
    
    const debouncedSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        // Фильтрация уже происходит через computed свойство
      }, 300)
    }
    
    const fetchServices = async () => {
      isLoading.value = true
      try {
        console.log('Загрузка услуг...')
        const response = await fitnessAPI.getAdminServices()
        services.value = response.data || []
        console.log('Услуги загружены:', services.value.length)
      } catch (error) {
        console.error('Error fetching services:', error)
        alert('Ошибка при загрузке услуг. Проверьте подключение к серверу.')
      } finally {
        isLoading.value = false
      }
    }
    
    const editService = (service) => {
      editingService.value = service
      serviceForm.value = { 
        name: service.name || '',
        description: service.description || '',
        price: service.price || '',
        duration: service.duration || '60'
      }
      showEditModal.value = true
      errorMessage.value = ''
    }
    
    const deleteService = async (id) => {
      if (!confirm('Вы уверены, что хотите удалить эту услугу? Все тренировки, связанные с этой услугой, могут стать недоступными.')) return
      
      try {
        await fitnessAPI.deleteService(id)
        alert('Услуга удалена успешно!')
        fetchServices()
      } catch (error) {
        console.error('Delete error:', error)
        alert('Ошибка при удалении услуги: ' + (error.response?.data?.detail || error.message))
      }
    }
    
    const saveService = async () => {
      isSaving.value = true
      errorMessage.value = ''
      
      try {
        // Валидация
        if (!serviceForm.value.name.trim()) {
          throw new Error('Название услуги обязательно')
        }
        
        // Подготовить данные для отправки
        const serviceData = {
          name: serviceForm.value.name.trim(),
          description: serviceForm.value.description?.trim() || null,
          price: serviceForm.value.price ? parseFloat(serviceForm.value.price) : 0.00,
          duration: serviceForm.value.duration ? parseInt(serviceForm.value.duration) : 60
        }
        
        console.log('Saving service data:', serviceData)
        
        if (editingService.value) {
          await fitnessAPI.updateService(editingService.value.id, serviceData)
          alert('Услуга обновлена успешно!')
        } else {
          await fitnessAPI.createService(serviceData)
          alert('Услуга создана успешно!')
        }
        
        closeModal()
        fetchServices()
      } catch (error) {
        console.error('Save service error:', error)
        
        // Обработка ошибок
        let errorMessageText = 'Неизвестная ошибка'
        if (error.response?.data?.detail) {
          errorMessageText = error.response.data.detail
        } else if (error.response?.data?.message) {
          errorMessageText = error.response.data.message
        } else if (error.message) {
          errorMessageText = error.message
        }
        
        errorMessage.value = errorMessageText
      } finally {
        isSaving.value = false
      }
    }
    
    const closeModal = () => {
      showCreateModal.value = false
      showEditModal.value = false
      editingService.value = null
      serviceForm.value = {
        name: '',
        description: '',
        price: '',
        duration: ''
      }
      errorMessage.value = ''
    }
    
    onMounted(() => {
      fetchServices()
    })
    
    return {
      services,
      isLoading,
      isSaving,
      showCreateModal,
      showEditModal,
      editingService,
      searchQuery,
      filteredServices,
      serviceForm,
      errorMessage,
      fetchServices,
      editService,
      deleteService,
      saveService,
      closeModal,
      debouncedSearch
    }
  }
}
</script>

<style scoped>
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.search-filter {
  margin-bottom: 20px;
  max-width: 400px;
}

.table {
  margin-top: 20px;
  background-color: var(--primary-dark);
  border-radius: var(--radius);
  overflow: hidden;
}

.table th {
  background-color: var(--secondary-dark);
  color: var(--accent-orange);
  font-weight: 600;
  padding: 15px;
  border: none;
}

.table td {
  padding: 15px;
  vertical-align: middle;
  border-top: 1px solid var(--border-color);
}

.description-truncate {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--text-muted);
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--text-muted);
}

.empty-state .btn {
  margin-top: 20px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background-color: var(--secondary-dark);
  border-radius: var(--radius);
  padding: 30px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h3 {
  margin: 0;
  color: var(--accent-orange);
}

.char-count {
  color: var(--text-muted);
  font-size: 0.85rem;
}

.form-text {
  color: var(--text-muted);
  font-size: 0.85rem;
  margin-top: 5px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}
</style>