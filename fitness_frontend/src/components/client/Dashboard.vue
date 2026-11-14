<template>
  <div class="container">
    <div class="dashboard-header">
      <h1 class="page-title">Личный кабинет</h1>
      <div class="welcome-message">
        Добро пожаловать, {{ user?.first_name || 'Пользователь' }}!
      </div>
    </div>
    
    <div class="dashboard-grid">
      <!-- Активные записи -->
      <div class="card dashboard-card">
        <div class="card-header">
          <h3>Мои записи</h3>
        </div>
        <div class="card-body">
          <div v-if="loadingRecords" class="loader"></div>
          <div v-else-if="records.length === 0" class="empty-state">
            <p>У вас нет активных записей</p>
            <router-link to="/schedule" class="btn btn-primary">
              Записаться на тренировку
            </router-link>
          </div>
          <div v-else>
            <div v-for="record in records.slice(0, 3)" :key="record.id" class="record-item">
              <div class="record-info">
                <strong>{{ record.workout?.service?.name }}</strong>
                <small>{{ formatDate(record.workout?.workout_date) }} {{ record.workout?.start_time }}</small>
              </div>
              <button @click="cancelRegistration(record.id)" class="btn btn-sm btn-danger">
                Отменить
              </button>
            </div>
            <router-link to="/schedule" class="btn btn-secondary" style="margin-top: 15px;">
              Все записи
            </router-link>
          </div>
        </div>
      </div>
      
      <!-- Активная подписка -->
      <div class="card dashboard-card">
        <div class="card-header">
          <h3>Моя подписка</h3>
        </div>
        <div class="card-body">
          <div v-if="loadingSubscription" class="loader"></div>
          <div v-else-if="!activeSubscription" class="empty-state">
            <p>У вас нет активной подписки</p>
            <router-link to="/subscriptions" class="btn btn-primary">
              Выбрать абонемент
            </router-link>
          </div>
          <div v-else>
            <div class="subscription-info">
              <h4>{{ activeSubscription.subscription?.subscription_type }}</h4>
              <p>Действует до: {{ formatDate(activeSubscription.end_action_date) }}</p>
              <p class="badge badge-success">Активна</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Быстрые действия -->
      <div class="card dashboard-card">
        <div class="card-header">
          <h3>Быстрые действия</h3>
        </div>
        <div class="card-body">
          <div class="quick-actions">
            <router-link to="/schedule" class="btn btn-primary">
              📅 Расписание
            </router-link>
            <router-link to="/centers" class="btn btn-secondary">
              🏋️ Залы
            </router-link>
            <router-link to="/services" class="btn btn-secondary">
              💪 Услуги
            </router-link>
            <router-link to="/profile" class="btn btn-secondary">
              👤 Профиль
            </router-link>
          </div>
        </div>
      </div>
      
      <!-- Статистика -->
      <div class="card dashboard-card">
        <div class="card-header">
          <h3>Статистика</h3>
        </div>
        <div class="card-body">
          <div class="stats">
            <div class="stat-item">
              <div class="stat-value">{{ stats.totalWorkouts || 0 }}</div>
              <div class="stat-label">Посещено тренировок</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ stats.activeSubscriptions || 0 }}</div>
              <div class="stat-label">Активных подписок</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { format } from 'date-fns'
import { fitnessAPI } from '../../services/api'
import { useAuthStore } from '../../store/auth'

export default {
  name: 'Dashboard',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const records = ref([])
    const activeSubscription = ref(null)
    const loadingRecords = ref(false)
    const loadingSubscription = ref(false)
    const stats = ref({})
    
    const user = computed(() => authStore.user)
    
    const fetchRecords = async () => {
      loadingRecords.value = true
      try {
        const response = await fitnessAPI.getClientRecords()
        records.value = response.data
      } catch (error) {
        console.error('Error fetching records:', error)
      } finally {
        loadingRecords.value = false
      }
    }
    
    const fetchSubscription = async () => {
      loadingSubscription.value = true
      try {
        const response = await fitnessAPI.getClientSubscriptions()
        if (response.data && response.data.length > 0) {
          // Находим активную подписку
          const today = new Date().toISOString().split('T')[0]
          activeSubscription.value = response.data.find(sub => 
            sub.end_action_date >= today && sub.start_action_date <= today
          )
        }
      } catch (error) {
        console.error('Error fetching subscription:', error)
      } finally {
        loadingSubscription.value = false
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return format(new Date(dateString), 'dd.MM.yyyy')
    }
    
    const cancelRegistration = async (recordId) => {
      if (!confirm('Вы уверены, что хотите отменить запись?')) return
      
      try {
        await fitnessAPI.cancelRegistration(recordId)
        alert('Запись отменена успешно!')
        fetchRecords()
      } catch (error) {
        alert(error.response?.data?.detail || 'Ошибка отмены записи')
      }
    }
    
    onMounted(() => {
      fetchRecords()
      fetchSubscription()
    })
    
    return {
      user,
      records,
      activeSubscription,
      loadingRecords,
      loadingSubscription,
      stats,
      formatDate,
      cancelRegistration
    }
  }
}
</script>

<style scoped>
.dashboard-header {
  margin-bottom: 30px;
}

.welcome-message {
  font-size: 1.2rem;
  color: var(--accent-orange);
  margin-top: 10px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.dashboard-card {
  height: 100%;
}

.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid var(--border-color);
}

.record-item:last-child {
  border-bottom: none;
}

.record-info {
  flex: 1;
}

.record-info small {
  color: var(--text-muted);
  display: block;
  margin-top: 5px;
}

.empty-state {
  text-align: center;
  padding: 20px 0;
}

.subscription-info {
  text-align: center;
}

.quick-actions {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}

.stats {
  display: flex;
  justify-content: space-around;
  text-align: center;
}

.stat-item {
  padding: 10px;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: var(--accent-orange);
}

.stat-label {
  color: var(--text-muted);
  font-size: 0.9rem;
}
</style>