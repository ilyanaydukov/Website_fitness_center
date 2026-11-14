<template>
  <div class="home">
    <section class="hero">
      <div class="container">
        <h1 class="hero-title">Добро пожаловать в Фитнес-центр</h1>
        <p class="hero-subtitle">
          Современное оборудование, профессиональные тренеры и лучшие условия для вашего здоровья
        </p>
        <div class="hero-actions">
          <router-link v-if="!isAuthenticated" to="/register" class="btn btn-primary btn-lg">
            Начать тренироваться
          </router-link>
          <router-link to="/schedule" class="btn btn-secondary btn-lg">
            Посмотреть расписание
          </router-link>
        </div>
      </div>
    </section>
    
    <section class="features">
      <div class="container">
        <h2 class="section-title">Наши возможности</h2>
        <div class="grid">
          <div class="card feature-card">
            <div class="feature-icon">🏋️</div>
            <h3>Тренировки</h3>
            <p>Разнообразные групповые и индивидуальные занятия</p>
          </div>
          
          <div class="card feature-card">
            <div class="feature-icon">👨‍🏫</div>
            <h3>Профессиональные тренеры</h3>
            <p>Опытные специалисты с индивидуальным подходом</p>
          </div>
          
          <div class="card feature-card">
            <div class="feature-icon">📅</div>
            <h3>Удобное расписание</h3>
            <p>Онлайн запись на занятия в любое время</p>
          </div>
          
          <div class="card feature-card">
            <div class="feature-icon">📊</div>
            <h3>Контроль прогресса</h3>
            <p>Отслеживайте свои результаты и достижения</p>
          </div>
        </div>
      </div>
    </section>
    
    <section class="stats">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-number">{{ stats.centers || '5' }}</div>
            <div class="stat-label">Фитнес-центров</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ stats.trainers || '20+' }}</div>
            <div class="stat-label">Профессиональных тренеров</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ stats.clients || '1000+' }}</div>
            <div class="stat-label">Довольных клиентов</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ stats.workouts || '50+' }}</div>
            <div class="stat-label">Тренировок в неделю</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { computed, ref, onMounted } from 'vue'
import { useAuthStore } from '../store/auth'
import { fitnessAPI } from '../services/api'

export default {
  name: 'Home',
  setup() {
    const authStore = useAuthStore()
    const stats = ref({})
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    
    const fetchStats = async () => {
      try {
        const [centersRes, trainersRes] = await Promise.all([
          fitnessAPI.getCenters(),
          fitnessAPI.getTrainers()
        ])
        
        stats.value = {
          centers: centersRes.data.length,
          trainers: trainersRes.data.length
        }
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    }
    
    onMounted(() => {
      fetchStats()
    })
    
    return {
      isAuthenticated,
      stats
    }
  }
}
</script>

<style scoped>
.hero {
  padding: 100px 0;
  text-align: center;
  background: linear-gradient(rgba(10, 10, 10, 0.9), rgba(26, 26, 26, 0.9)), 
              url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
  background-size: cover;
  background-position: center;
  color: white;
}

.hero-title {
  font-size: 3rem;
  margin-bottom: 20px;
  background: linear-gradient(to right, var(--accent-orange), var(--accent-purple));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.hero-subtitle {
  font-size: 1.2rem;
  margin-bottom: 40px;
  color: var(--text-muted);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.section-title {
  font-size: 2.5rem;
  text-align: center;
  margin: 60px 0 40px;
  color: var(--text-light);
}

.features {
  padding: 60px 0;
}

.feature-card {
  text-align: center;
  padding: 30px;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.feature-card h3 {
  color: var(--accent-orange);
  margin-bottom: 15px;
}

.stats {
  padding: 80px 0;
  background: linear-gradient(135deg, var(--primary-dark) 0%, #2a2a2a 100%);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
  text-align: center;
}

.stat-item {
  padding: 30px;
}

.stat-number {
  font-size: 3rem;
  font-weight: 700;
  color: var(--accent-orange);
  margin-bottom: 10px;
}

.stat-label {
  font-size: 1.1rem;
  color: var(--text-muted);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>