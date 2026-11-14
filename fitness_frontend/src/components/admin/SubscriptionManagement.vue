<template>
  <div class="container">
    <div class="admin-header">
      <h1 class="page-title">Управление абонементами</h1>
      <button @click="showCreateModal = true" class="btn btn-primary">
        + Добавить абонемент
      </button>
    </div>
    
    <div v-if="isLoading" class="loader"></div>
    
    <div v-else>
      <div class="search-filter">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Поиск по типу абонемента..."
          class="form-control"
          @input="debouncedSearch"
        />
      </div>
      
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Тип абонемента</th>
            <th>Описание</th>
            <th>Цена (₽)</th>
            <th>Срок действия</th>
            <th>Уровень доступа</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="subscription in filteredSubscriptions" :key="subscription.id">
            <td>{{ subscription.id }}</td>
            <td>
              <strong>{{ subscription.subscription_type }}</strong>
            </td>
            <td>
              <div class="description-truncate">
                {{ subscription.description || subscription.access_description || 'Нет описания' }}
              </div>
            </td>
            <td>{{ subscription.price ? subscription.price.toFixed(2) : '0.00' }}</td>
            <td>{{ subscription.validity_period }} дней</td>
            <td>
              <span class="badge" :class="getAccessLevelClass(subscription.subscription_access_level_id)">
                {{ getAccessLevelName(subscription.subscription_access_level_id) }}
              </span>
            </td>
            <td>
              <button @click="editSubscription(subscription)" class="btn btn-sm btn-secondary me-2">
                Редактировать
              </button>
              <button @click="deleteSubscription(subscription.id)" class="btn btn-sm btn-danger">
                Удалить
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="filteredSubscriptions.length === 0" class="empty-state">
        <p>{{ searchQuery ? 'Абонементы не найдены по запросу' : 'Абонементы не найдены' }}</p>
        <button @click="showCreateModal = true" class="btn btn-primary">
          Создать первый абонемент
        </button>
      </div>
    </div>
    
    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editingSubscription ? 'Редактировать' : 'Добавить' }} абонемент</h3>
          <button @click="closeModal" class="btn btn-sm btn-danger">&times;</button>
        </div>
        
        <form @submit.prevent="saveSubscription" class="modal-form">
          <div class="form-group mb-3">
            <label class="form-label">Тип абонемента *</label>
            <input 
              type="text" 
              v-model="subscriptionForm.subscription_type" 
              required 
              class="form-control" 
              placeholder="Например: Базовый, Премиум, Годовой"
            />
          </div>
          
          <div class="form-group mb-3">
            <label class="form-label">Описание</label>
            <textarea 
              v-model="subscriptionForm.description" 
              class="form-control" 
              rows="3"
              placeholder="Подробное описание абонемента, что входит..."
              maxlength="500"
            ></textarea>
            <div class="char-count text-end mt-1">
              {{ subscriptionForm.description?.length || 0 }}/500 символов
            </div>
          </div>
          
          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Цена (₽) *</label>
              <input 
                type="number" 
                v-model="subscriptionForm.price" 
                required 
                class="form-control" 
                min="0" 
                step="0.01"
                placeholder="0.00"
              />
              <small class="form-text text-muted">0.00 - если бесплатный</small>
            </div>
            <div class="col-md-6">
              <label class="form-label">Срок действия (дней) *</label>
              <input 
                type="number" 
                v-model="subscriptionForm.validity_period" 
                required 
                class="form-control" 
                min="1"
                placeholder="30"
              />
              <small class="form-text text-muted">Количество дней действия абонемента</small>
            </div>
          </div>
          
          <div class="form-group mb-3">
            <label class="form-label">Уровень доступа *</label>
            <select v-model="subscriptionForm.subscription_access_level_id" required class="form-control">
              <option value="">Выберите уровень доступа</option>
              <option v-for="level in accessLevels" :key="level.id" :value="level.id">
                {{ level.access_level_name }} ({{ level.access_description || 'без описания' }})
              </option>
            </select>
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
  name: 'SubscriptionManagement',
  setup() {
    const subscriptions = ref([])
    const accessLevels = ref([])
    const isLoading = ref(false)
    const isSaving = ref(false)
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const editingSubscription = ref(null)
    const searchQuery = ref('')
    const errorMessage = ref('')
    let searchTimeout = null
    
    const subscriptionForm = ref({
      subscription_type: '',
      description: '',
      price: '',
      validity_period: '',
      subscription_access_level_id: ''
    })
    
    const filteredSubscriptions = computed(() => {
      if (!searchQuery.value.trim()) return subscriptions.value
      
      const query = searchQuery.value.toLowerCase().trim()
      return subscriptions.value.filter(subscription => 
        subscription.subscription_type?.toLowerCase().includes(query) ||
        subscription.description?.toLowerCase().includes(query)
      )
    })
    
    const debouncedSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        // Фильтрация уже происходит через computed свойство
      }, 300)
    }
    
    const fetchData = async () => {
      isLoading.value = true
      try {
        // Получаем абонементы
        const response = await fitnessAPI.getSubscriptions()
        subscriptions.value = response.data || []
        
        console.log('Абонементы загружены:', subscriptions.value)
        
        // Получаем уровни доступа
        await fetchAccessLevels()
        
      } catch (error) {
        console.error('Error fetching subscriptions:', error)
        errorMessage.value = 'Не удалось загрузить абонементы. Проверьте подключение к серверу.'
      } finally {
        isLoading.value = false
      }
    }
    
    const fetchAccessLevels = async () => {
      try {
        // Пробуем получить уровни доступа из API
        const response = await api.get('/subscriptions/access-levels')
        accessLevels.value = response.data || []
      } catch (error) {
        console.log('Не удалось загрузить уровни доступа из API, используем статические:', error)
        // Статические данные для уровней доступа (важно: ID должны соответствовать ID в базе данных)
        accessLevels.value = [
          { 
            id: 1, 
            access_level_name: 'Базовый', 
            access_description: 'Доступ к тренажерному залу в часы работы',
            created_at: null,
            updated_at: null
          },
          { 
            id: 2, 
            access_level_name: 'Стандартный', 
            access_description: 'Доступ к залу и групповым занятиям',
            created_at: null,
            updated_at: null
          },
          { 
            id: 3, 
            access_level_name: 'Премиум', 
            access_description: 'Полный доступ + персональные тренировки',
            created_at: null,
            updated_at: null
          },
          { 
            id: 4, 
            access_level_name: 'VIP', 
            access_description: 'Все включено + спа зона + индивидуальный тренер',
            created_at: null,
            updated_at: null
          }
        ]
      }
      
      console.log('Уровни доступа:', accessLevels.value)
    }
    
    const getAccessLevelName = (levelId) => {
      if (!levelId) return 'Не указан'
      
      const level = accessLevels.value.find(l => l.id === levelId)
      return level ? level.access_level_name : `Уровень ${levelId}`
    }
    
    const getAccessLevelClass = (levelId) => {
      const level = accessLevels.value.find(l => l.id === levelId)
      if (!level) return 'badge-secondary'
      
      switch(levelId) {
        case 1: return 'badge-info'
        case 2: return 'badge-primary'
        case 3: return 'badge-warning'
        case 4: return 'badge-danger'
        default: return 'badge-secondary'
      }
    }
    
    const editSubscription = (subscription) => {
      editingSubscription.value = subscription
      subscriptionForm.value = { 
        subscription_type: subscription.subscription_type || '',
        description: subscription.description || subscription.access_description || '',
        price: subscription.price || '',
        validity_period: subscription.validity_period || '',
        subscription_access_level_id: subscription.subscription_access_level_id || ''
      }
      showEditModal.value = true
      errorMessage.value = ''
    }
    
    const deleteSubscription = async (id) => {
      if (!confirm('Вы уверены, что хотите удалить этот абонемент? Существующие подписки клиентов останутся активными, но новые клиенты не смогут его приобрести.')) return
      
      try {
        await fitnessAPI.deleteSubscription(id)
        alert('Абонемент удален успешно!')
        fetchData()
      } catch (error) {
        console.error('Delete error:', error)
        alert('Ошибка при удалении абонемента: ' + (error.response?.data?.detail || error.message))
      }
    }
    
    const saveSubscription = async () => {
      isSaving.value = true
      errorMessage.value = ''
      
      try {
        // Валидация
        if (!subscriptionForm.value.subscription_type.trim()) {
          throw new Error('Тип абонемента обязателен')
        }
        
        if (!subscriptionForm.value.price || parseFloat(subscriptionForm.value.price) < 0) {
          throw new Error('Цена должна быть положительным числом или 0')
        }
        
        if (!subscriptionForm.value.validity_period || parseInt(subscriptionForm.value.validity_period) < 1) {
          throw new Error('Срок действия должен быть не менее 1 дня')
        }
        
        if (!subscriptionForm.value.subscription_access_level_id) {
          throw new Error('Выберите уровень доступа')
        }
        
        // Проверяем, что выбранный уровень доступа существует
        const selectedLevel = accessLevels.value.find(
          level => level.id === parseInt(subscriptionForm.value.subscription_access_level_id)
        )
        
        if (!selectedLevel) {
          throw new Error('Выбранный уровень доступа не существует')
        }
        
        // Подготовить данные для отправки
        const subscriptionData = {
          subscription_type: subscriptionForm.value.subscription_type.trim(),
          description: subscriptionForm.value.description?.trim() || null,
          price: parseFloat(subscriptionForm.value.price) || 0,
          validity_period: parseInt(subscriptionForm.value.validity_period) || 30,
          subscription_access_level_id: parseInt(subscriptionForm.value.subscription_access_level_id)
        }
        
        console.log('Saving subscription data:', subscriptionData)
        
        if (editingSubscription.value) {
          await fitnessAPI.updateSubscription(editingSubscription.value.id, subscriptionData)
          alert('Абонемент обновлен успешно!')
        } else {
          await fitnessAPI.createSubscription(subscriptionData)
          alert('Абонемент создан успешно!')
        }
        
        closeModal()
        fetchData()
      } catch (error) {
        console.error('Save subscription error:', error)
        
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
      editingSubscription.value = null
      subscriptionForm.value = {
        subscription_type: '',
        description: '',
        price: '',
        validity_period: '',
        subscription_access_level_id: ''
      }
      errorMessage.value = ''
    }
    
    onMounted(() => {
      fetchData()
    })
    
    return {
      subscriptions,
      accessLevels,
      isLoading,
      isSaving,
      showCreateModal,
      showEditModal,
      editingSubscription,
      searchQuery,
      filteredSubscriptions,
      subscriptionForm,
      errorMessage,
      fetchData,
      getAccessLevelName,
      getAccessLevelClass,
      editSubscription,
      deleteSubscription,
      saveSubscription,
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

.badge {
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.badge-info {
  background-color: #17a2b8;
  color: white;
}

.badge-primary {
  background-color: #007bff;
  color: white;
}

.badge-warning {
  background-color: #ffc107;
  color: #212529;
}

.badge-danger {
  background-color: #dc3545;
  color: white;
}

.badge-secondary {
  background-color: #6c757d;
  color: white;
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