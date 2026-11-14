<template>
  <div class="container">
    <h1 class="page-title">Административная панель</h1>
    
    <div class="admin-welcome">
      <h2>Добро пожаловать, Администратор!</h2>
      <p>Здесь вы можете управлять всеми аспектами фитнес-центра</p>
    </div>
    
    <div class="admin-stats">
      <div class="stats-grid">
        <div class="stat-card card">
          <div class="stat-icon">👥</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.clients || '0' }}</div>
            <div class="stat-label">Клиентов</div>
          </div>
        </div>
        
        <div class="stat-card card">
          <div class="stat-icon">🏋️</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.workouts || '0' }}</div>
            <div class="stat-label">Тренировок</div>
          </div>
        </div>
        
        <div class="stat-card card">
          <div class="stat-icon">👨‍🏫</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.trainers || '0' }}</div>
            <div class="stat-label">Тренеров</div>
          </div>
        </div>
        
        <div class="stat-card card">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.subscriptions || '0' }}</div>
            <div class="stat-label">Абонементов</div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="admin-actions">
      <h3>Быстрые действия</h3>
      <div class="actions-grid">
        <router-link to="/admin/workouts" class="action-card card">
          <div class="action-icon">📅</div>
          <h4>Расписание</h4>
          <p>Управление тренировками</p>
        </router-link>
        
        <router-link to="/admin/trainers" class="action-card card">
          <div class="action-icon">👨‍🏫</div>
          <h4>Тренеры</h4>
          <p>Управление тренерским штатом</p>
        </router-link>
        
        <router-link to="/admin/services" class="action-card card">
          <div class="action-icon">💪</div>
          <h4>Услуги</h4>
          <p>Управление услугами</p>
        </router-link>
        
        <router-link to="/admin/subscriptions" class="action-card card">
          <div class="action-icon">💰</div>
          <h4>Абонементы</h4>
          <p>Управление абонементами</p>
        </router-link>
        
        <router-link to="/admin/reports" class="action-card card">
          <div class="action-icon">📊</div>
          <h4>Отчеты</h4>
          <p>Генерация отчетов</p>
        </router-link>
      </div>
    </div>
    
    <div class="recent-activities">
      <h3>Последние действия</h3>
      <div class="activities-list">
        <div v-if="activities.length === 0" class="empty-state">
          <p>Нет недавних действий</p>
        </div>
        <div v-else>
          <div v-for="activity in activities" :key="activity.id" class="activity-item">
            <div class="activity-icon">
              <span v-if="activity.type === 'workout'">📅</span>
              <span v-if="activity.type === 'trainer'">👨‍🏫</span>
              <span v-if="activity.type === 'service'">💪</span>
            </div>
            <div class="activity-content">
              <p>{{ activity.message }}</p>
              <small>{{ formatTime(activity.timestamp) }}</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { format } from 'date-fns'
import { fitnessAPI } from '../../services/api'

export default {
  name: 'AdminDashboard',
  setup() {
    const stats = ref({})
    const activities = ref([])
    const isLoading = ref(false)
    
    const fetchStats = async () => {
      isLoading.value = true
      try {
        // Здесь нужно получить статистику из API
        // В текущем API нет готового эндпоинта, но можно собрать из разных
        const [workoutsRes, trainersRes, servicesRes] = await Promise.all([
          fitnessAPI.getWorkouts(),
          fitnessAPI.getTrainers(),
          fitnessAPI.getServices()
        ])
        
        stats.value = {
          workouts: workoutsRes.data.length,
          trainers: trainersRes.data.length,
          services: servicesRes.data.length
        }
      } catch (error) {
        console.error('Error fetching stats:', error)
      } finally {
        isLoading.value = false
      }
    }
    
    const formatTime = (timestamp) => {
      return format(new Date(timestamp), 'HH:mm dd.MM.yyyy')
    }
    
    onMounted(() => {
      fetchStats()
      
      // Заглушка для активности
      activities.value = [
        {
          id: 1,
          type: 'workout',
          message: 'Добавлена новая тренировка "Йога для начинающих"',
          timestamp: new Date().toISOString()
        },
        {
          id: 2,
          type: 'trainer',
          message: 'Обновлена информация о тренере Иване Иванове',
          timestamp: new Date(Date.now() - 3600000).toISOString()
        }
      ]
    })
    
    return {
      stats,
      activities,
      isLoading,
      formatTime
    }
  }
}
</script>

<style scoped>
.admin-welcome {
  text-align: center;
  margin-bottom: 40px;
  padding: 30px;
  background: linear-gradient(135deg, var(--primary-dark) 0%, #2a2a2a 100%);
  border-radius: var(--radius);
}

.admin-welcome h2 {
  color: var(--accent-orange);
  margin-bottom: 10px;
}

.admin-welcome p {
  color: var(--text-muted);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: var(--accent-orange);
  margin-bottom: 5px;
}

.stat-label {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.admin-actions {
  margin-bottom: 40px;
}

.admin-actions h3 {
  color: var(--accent-orange);
  margin-bottom: 20px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.action-card {
  padding: 30px;
  text-align: center;
  text-decoration: none;
  color: inherit;
  transition: transform 0.3s ease;
}

.action-card:hover {
  transform: translateY(-5px);
  border-color: var(--accent-orange);
}

.action-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.action-card h4 {
  color: var(--accent-orange);
  margin-bottom: 10px;
}

.action-card p {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.recent-activities h3 {
  color: var(--accent-orange);
  margin-bottom: 20px;
}

.activities-list {
  background-color: var(--secondary-dark);
  border-radius: var(--radius);
  padding: 20px;
}

.empty-state {
  text-align: center;
  padding: 30px;
  color: var(--text-muted);
}

.activity-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  border-bottom: 1px solid var(--border-color);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  font-size: 1.5rem;
}

.activity-content {
  flex: 1;
}

.activity-content p {
  margin-bottom: 5px;
  color: var(--text-light);
}

.activity-content small {
  color: var(--text-muted);
}
</style>