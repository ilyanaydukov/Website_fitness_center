<template>
  <div class="container">
    <h1 class="page-title">Абонементы</h1>
    
    <div v-if="isLoading" class="loader"></div>
    
    <div v-else class="subscriptions-container">
      <!-- Активная подписка -->
      <div v-if="activeSubscription" class="card active-subscription mb-4">
        <div class="card-header bg-success text-white">
          <div class="d-flex justify-content-between align-items-center">
            <h3 class="mb-0">Ваш активный абонемент</h3>
            <span class="badge bg-light text-success">Активен</span>
          </div>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-8">
              <h4 class="text-primary">{{ activeSubscription.subscription?.subscription_type || 'Абонемент' }}</h4>
              
              <div class="subscription-details mt-3">
                <div class="detail-item mb-2">
                  <span class="detail-label">Действует с:</span>
                  <span class="detail-value">{{ formatDate(activeSubscription.start_action_date) }}</span>
                </div>
                <div class="detail-item mb-2">
                  <span class="detail-label">Действует до:</span>
                  <span class="detail-value">{{ formatDate(activeSubscription.end_action_date) }}</span>
                </div>
                <div class="detail-item mb-2">
                  <span class="detail-label">Стоимость:</span>
                  <span class="detail-value fw-bold text-success">
                    {{ activeSubscription.subscription?.price?.toFixed(2) || '0.00' }} ₽
                  </span>
                </div>
                <div class="detail-item mb-2">
                  <span class="detail-label">Срок действия:</span>
                  <span class="detail-value">{{ activeSubscription.subscription?.validity_period || '30' }} дней</span>
                </div>
                <div v-if="activeSubscription.subscription?.access_description" class="detail-item mt-3">
                  <span class="detail-label">Что входит:</span>
                  <p class="detail-value mt-1">{{ activeSubscription.subscription.access_description }}</p>
                </div>
              </div>
            </div>
            
            <div class="col-md-4">
              <div class="progress-container">
                <div class="text-center mb-3">
                  <div class="display-4 fw-bold text-primary">{{ daysLeft }}</div>
                  <div class="text-muted">дней осталось</div>
                </div>
                
                <div class="progress mb-2" style="height: 10px;">
                  <div 
                    class="progress-bar bg-success" 
                    :style="{ width: daysLeftPercent + '%' }"
                    role="progressbar"
                  ></div>
                </div>
                
                <div class="d-flex justify-content-between text-muted small">
                  <span>0 дней</span>
                  <span>{{ activeSubscription.subscription?.validity_period || '30' }} дней</span>
                </div>
                
                <div class="text-center mt-4">
                  <div class="text-muted small">Прогресс использования</div>
                  <div class="h5">{{ daysLeftPercent.toFixed(0) }}%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Доступные абонементы -->
      <div class="available-subscriptions">
        <div class="section-header mb-4">
          <h2>Доступные абонементы</h2>
          <p class="text-muted">Выберите подходящий абонемент для занятий в нашем фитнес-центре</p>
          
          <div v-if="hasActiveSubscription" class="alert alert-info">
            <div class="d-flex align-items-center">
              <i class="bi bi-info-circle me-2"></i>
              <div>
                У вас уже есть активный абонемент. Новый абонемент можно будет приобрести после окончания текущего.
                <div class="mt-1 small">
                  Истекает: {{ formatDate(activeSubscription.end_action_date) }} 
                  (через {{ daysLeft }} дней)
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="subscriptions.length === 0" class="alert alert-warning">
          <div class="d-flex align-items-center">
            <i class="bi bi-exclamation-triangle me-2"></i>
            <div>Нет доступных абонементов. Обратитесь к администратору или попробуйте позже.</div>
          </div>
        </div>
        
        <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          <div v-for="subscription in subscriptions" :key="subscription.id" class="col">
            <div class="card subscription-card h-100">
              <div class="card-header bg-light">
                <div class="d-flex justify-content-between align-items-center">
                  <h4 class="card-title mb-0 text-primary">{{ subscription.subscription_type }}</h4>
                  <span class="badge" :class="getAccessLevelBadgeClass(subscription.subscription_access_level_id)">
                    {{ getAccessLevelName(subscription.subscription_access_level_id) }}
                  </span>
                </div>
              </div>
              
              <div class="card-body d-flex flex-column">
                <div class="price-section text-center mb-4">
                  <div class="display-4 fw-bold text-success">
                    {{ subscription.price?.toFixed(2) || '0.00' }} ₽
                  </div>
                  <div class="text-muted">
                    за {{ subscription.validity_period }} дней
                  </div>
                </div>
                
                <div class="features-section flex-grow-1">
                  <div v-if="subscription.description || subscription.access_description" class="mb-3">
                    <h6 class="text-muted mb-2">Что входит:</h6>
                    <p class="card-text">{{ subscription.description || subscription.access_description }}</p>
                  </div>
                  
                  <div class="benefits-list">
                    <div class="benefit-item mb-2">
                      <i class="bi bi-check-circle-fill text-success me-2"></i>
                      <span>Срок действия: {{ subscription.validity_period }} дней</span>
                    </div>
                    <div class="benefit-item mb-2">
                      <i class="bi bi-check-circle-fill text-success me-2"></i>
                      <span>Уровень доступа: {{ getAccessLevelName(subscription.subscription_access_level_id) }}</span>
                    </div>
                    <div class="benefit-item mb-2">
                      <i class="bi bi-check-circle-fill text-success me-2"></i>
                      <span>Доступ ко всем залам центра</span>
                    </div>
                  </div>
                </div>
                
                <div class="card-footer bg-transparent border-0 pt-3">
                  <div class="d-grid gap-2">
                    <button 
                      @click="purchaseSubscription(subscription)" 
                      class="btn btn-primary btn-lg"
                      :disabled="hasActiveSubscription"
                    >
                      {{ hasActiveSubscription ? 'Уже есть абонемент' : 'Приобрести сейчас' }}
                    </button>
                    
                    <button 
                      @click="viewSubscriptionDetails(subscription)"
                      class="btn btn-outline-secondary"
                    >
                      <i class="bi bi-info-circle me-2"></i>
                      Подробнее
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Subscription Details Modal -->
    <div v-if="showDetailsModal" class="modal fade show" style="display: block; background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedSubscription?.subscription_type }}</h5>
            <button type="button" class="btn-close" @click="closeDetailsModal"></button>
          </div>
          
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6">
                <div class="card mb-3">
                  <div class="card-body text-center">
                    <div class="display-3 fw-bold text-success">
                      {{ selectedSubscription?.price?.toFixed(2) || '0.00' }} ₽
                    </div>
                    <div class="h5 text-muted">
                      за {{ selectedSubscription?.validity_period }} дней
                    </div>
                  </div>
                </div>
                
                <div class="card">
                  <div class="card-header">
                    <h6 class="mb-0">Основная информация</h6>
                  </div>
                  <div class="card-body">
                    <table class="table table-sm">
                      <tbody>
                        <tr>
                          <td><strong>Тип:</strong></td>
                          <td>{{ selectedSubscription?.subscription_type }}</td>
                        </tr>
                        <tr>
                          <td><strong>Цена:</strong></td>
                          <td class="fw-bold text-success">{{ selectedSubscription?.price?.toFixed(2) || '0.00' }} ₽</td>
                        </tr>
                        <tr>
                          <td><strong>Срок действия:</strong></td>
                          <td>{{ selectedSubscription?.validity_period }} дней</td>
                        </tr>
                        <tr>
                          <td><strong>Уровень доступа:</strong></td>
                          <td>
                            <span class="badge" :class="getAccessLevelBadgeClass(selectedSubscription?.subscription_access_level_id)">
                              {{ getAccessLevelName(selectedSubscription?.subscription_access_level_id) }}
                            </span>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
              
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6 class="mb-0">Что входит в абонемент</h6>
                  </div>
                  <div class="card-body">
                    <div v-if="selectedSubscription?.description || selectedSubscription?.access_description" class="mb-4">
                      <p>{{ selectedSubscription?.description || selectedSubscription?.access_description }}</p>
                    </div>
                    
                    <h6 class="mb-3">Преимущества:</h6>
                    <div class="benefits-list-detailed">
                      <div class="benefit-detailed mb-3">
                        <div class="benefit-icon">
                          <i class="bi bi-check-circle-fill text-success"></i>
                        </div>
                        <div class="benefit-content">
                          <strong>Неограниченное посещение</strong>
                          <p class="text-muted small mb-0">Посещайте фитнес-центр неограниченное количество раз в период действия абонемента</p>
                        </div>
                      </div>
                      
                      <div class="benefit-detailed mb-3">
                        <div class="benefit-icon">
                          <i class="bi bi-check-circle-fill text-success"></i>
                        </div>
                        <div class="benefit-content">
                          <strong>Доступ ко всем залам</strong>
                          <p class="text-muted small mb-0">Тренажерный зал, кардио-зона, зона групповых занятий</p>
                        </div>
                      </div>
                      
                      <div class="benefit-detailed mb-3">
                        <div class="benefit-icon">
                          <i class="bi bi-check-circle-fill text-success"></i>
                        </div>
                        <div class="benefit-content">
                          <strong>Расписание тренировок</strong>
                          <p class="text-muted small mb-0">Доступ к полному расписанию групповых занятий</p>
                        </div>
                      </div>
                      
                      <div class="benefit-detailed">
                        <div class="benefit-icon">
                          <i class="bi bi-check-circle-fill text-success"></i>
                        </div>
                        <div class="benefit-content">
                          <strong>Персональная консультация</strong>
                          <p class="text-muted small mb-0">Бесплатная первичная консультация с тренером</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDetailsModal">
              Закрыть
            </button>
            <button 
              type="button" 
              class="btn btn-primary"
              @click="purchaseSubscription(selectedSubscription)"
              :disabled="hasActiveSubscription"
            >
              {{ hasActiveSubscription ? 'Абонемент уже активен' : 'Приобрести' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { format, differenceInDays, parseISO } from 'date-fns'
import { fitnessAPI } from '../../services/api'

export default {
  name: 'Subscriptions',
  setup() {
    const subscriptions = ref([])
    const clientSubscriptions = ref([])
    const isLoading = ref(false)
    const isPurchasing = ref(false)
    const showDetailsModal = ref(false)
    const selectedSubscription = ref(null)
    
    // Статические уровни доступа
    const accessLevels = ref([
      { id: 1, name: 'Базовый', description: 'Доступ к тренажерному залу' },
      { id: 2, name: 'Стандартный', description: 'Доступ к залу и групповым занятиям' },
      { id: 3, name: 'Премиум', description: 'Полный доступ + персональные тренировки' },
      { id: 4, name: 'VIP', description: 'Все включено + спа зона' }
    ])
    
    const fetchData = async () => {
      isLoading.value = true
      try {
        console.log('Загрузка абонементов...')
        
        // Загружаем все доступные абонементы
        const [subscriptionsRes, clientSubscriptionsRes] = await Promise.all([
          fitnessAPI.getSubscriptions(),
          fetchClientSubscriptions()
        ])
        
        subscriptions.value = subscriptionsRes.data || []
        clientSubscriptions.value = clientSubscriptionsRes || []
        
        console.log('Доступные абонементы:', subscriptions.value)
        console.log('Абонементы клиента:', clientSubscriptions.value)
        
      } catch (error) {
        console.error('Error fetching subscriptions:', error)
        alert('Ошибка загрузки данных: ' + (error.response?.data?.detail || error.message))
      } finally {
        isLoading.value = false
      }
    }
    
    const fetchClientSubscriptions = async () => {
      try {
        // Пробуем получить активные подписки клиента
        const response = await fitnessAPI.getClientSubscriptions()
        return response.data || []
      } catch (error) {
        console.log('У клиента еще нет абонементов или ошибка загрузки:', error)
        return []
      }
    }
    
    const activeSubscription = computed(() => {
      if (!clientSubscriptions.value || clientSubscriptions.value.length === 0) {
        return null
      }
      
      const today = new Date()
      return clientSubscriptions.value.find(sub => {
        const startDate = parseISO(sub.start_action_date)
        const endDate = parseISO(sub.end_action_date)
        return today >= startDate && today <= endDate
      })
    })
    
    const hasActiveSubscription = computed(() => {
      return !!activeSubscription.value
    })
    
    const daysLeft = computed(() => {
      if (!activeSubscription.value) return 0
      
      try {
        const endDate = parseISO(activeSubscription.value.end_action_date)
        const today = new Date()
        const diff = differenceInDays(endDate, today)
        return Math.max(0, diff)
      } catch (error) {
        return 0
      }
    })
    
    const daysLeftPercent = computed(() => {
      if (!activeSubscription.value || !activeSubscription.value.subscription?.validity_period) {
        return 0
      }
      
      const validityPeriod = activeSubscription.value.subscription.validity_period
      if (validityPeriod <= 0) return 0
      
      const remaining = daysLeft.value
      const used = validityPeriod - remaining
      return (used / validityPeriod) * 100
    })
    
    const getAccessLevelName = (levelId) => {
      if (!levelId) return 'Не указан'
      
      const level = accessLevels.value.find(l => l.id === levelId)
      return level ? level.name : `Уровень ${levelId}`
    }
    
    const getAccessLevelBadgeClass = (levelId) => {
      switch(levelId) {
        case 1: return 'bg-info'
        case 2: return 'bg-primary'
        case 3: return 'bg-warning text-dark'
        case 4: return 'bg-danger'
        default: return 'bg-secondary'
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Не указана'
      try {
        return format(parseISO(dateString), 'dd.MM.yyyy')
      } catch (error) {
        return dateString
      }
    }
    
    const purchaseSubscription = async (subscription) => {
      if (hasActiveSubscription.value) {
        alert('У вас уже есть активный абонемент. Новый можно будет приобрести после ' + 
              formatDate(activeSubscription.value.end_action_date))
        return
      }
      
      if (!confirm(`Вы уверены, что хотите приобрести абонемент "${subscription.subscription_type}" за ${subscription.price} ₽?`)) {
        return
      }
      
      isPurchasing.value = true
      try {
        // Создаем новую подписку клиента
        const startDate = new Date()
        const endDate = new Date(startDate)
        endDate.setDate(endDate.getDate() + (subscription.validity_period || 30))
        
        const clientSubscriptionData = {
          subscription_id: subscription.id,
          start_action_date: startDate.toISOString().split('T')[0],
          end_action_date: endDate.toISOString().split('T')[0],
          subscription_activity_id: 1 // Активная
        }
        
        console.log('Создаем подписку клиента:', clientSubscriptionData)
        
        // Пробуем отправить запрос на создание подписки
        try {
          const response = await api.post('/client-subscriptions', clientSubscriptionData)
          alert('Абонемент успешно приобретен!')
          await fetchData() // Обновляем данные
          showDetailsModal.value = false
        } catch (apiError) {
          // Если эндпоинт не работает, показываем информацию для покупки
          console.log('API эндпоинт недоступен, показываем информацию для покупки', apiError)
          alert(`Абонемент "${subscription.subscription_type}" выбран. Для завершения покупки обратитесь к администратору.`)
        }
        
      } catch (error) {
        console.error('Purchase error:', error)
        alert('Ошибка при покупке абонемента: ' + (error.response?.data?.detail || error.message))
      } finally {
        isPurchasing.value = false
      }
    }
    
    const viewSubscriptionDetails = (subscription) => {
      selectedSubscription.value = subscription
      showDetailsModal.value = true
    }
    
    const closeDetailsModal = () => {
      showDetailsModal.value = false
      selectedSubscription.value = null
    }
    
    onMounted(() => {
      fetchData()
    })
    
    return {
      subscriptions,
      clientSubscriptions,
      isLoading,
      isPurchasing,
      showDetailsModal,
      selectedSubscription,
      activeSubscription,
      hasActiveSubscription,
      daysLeft,
      daysLeftPercent,
      formatDate,
      getAccessLevelName,
      getAccessLevelBadgeClass,
      purchaseSubscription,
      viewSubscriptionDetails,
      closeDetailsModal
    }
  }
}
</script>

<style scoped>
.subscriptions-container {
  max-width: 1200px;
  margin: 0 auto;
}

.active-subscription {
  border: 2px solid #28a745;
  box-shadow: 0 0 20px rgba(40, 167, 69, 0.1);
}

.section-header {
  padding: 20px 0;
  border-bottom: 2px solid #f0f0f0;
  margin-bottom: 30px;
}

.subscription-card {
  transition: all 0.3s ease;
  border: 1px solid #dee2e6;
  height: 100%;
}

.subscription-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  border-color: #007bff;
}

.price-section {
  padding: 20px 0;
}

.features-section {
  min-height: 200px;
}

.benefits-list .benefit-item {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
}

.benefits-list-detailed .benefit-detailed {
  display: flex;
  gap: 15px;
  align-items: flex-start;
}

.benefits-list-detailed .benefit-icon {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.benefits-list-detailed .benefit-content {
  flex: 1;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  color: #6c757d;
  font-weight: 500;
}

.detail-value {
  color: #212529;
  font-weight: 400;
}

.progress-container {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #e9ecef;
}

.loader {
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 2s linear infinite;
  margin: 50px auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.modal {
  z-index: 1050;
}

.modal-backdrop {
  z-index: 1040;
}

.badge {
  padding: 6px 12px;
  font-size: 0.8rem;
  font-weight: 600;
}
</style>