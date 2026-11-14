<template>
  <div class="container">
    <h1 class="page-title">Наши тренеры</h1>
    
    <div class="filters card">
      <div class="row">
        <div class="col">
          <label class="form-label">Специализация:</label>
          <select v-model="filters.specializationId" class="form-control">
            <option value="">Все специализации</option>
            <option v-for="spec in specializations" :key="spec.id" :value="spec.id">
              {{ spec.name }}
            </option>
          </select>
        </div>
        <div class="col">
          <label class="form-label">Опыт (лет):</label>
          <input type="number" v-model="filters.minExperience" class="form-control" placeholder="От" min="0" />
        </div>
      </div>
      <button @click="applyFilters" class="btn btn-primary">Применить</button>
      <button @click="resetFilters" class="btn btn-secondary">Сбросить</button>
    </div>
    
    <div v-if="isLoading" class="loader"></div>
    
    <div v-else class="trainers-grid">
      <div v-for="trainer in filteredTrainers" :key="trainer.id" class="card trainer-card">
        <div class="trainer-header">
          <h3>{{ trainer.first_name }} {{ trainer.last_name }}</h3>
          <span class="specialization">{{ trainer.specialization?.name || 'Тренер' }}</span>
        </div>
        
        <div class="trainer-info">
          <p v-if="trainer.work_experience">
            <strong>Опыт работы:</strong> {{ trainer.work_experience }} лет
          </p>
          <p v-if="trainer.specialization?.description">
            <strong>Специализация:</strong> {{ trainer.specialization.description }}
          </p>
          <p v-if="trainer.email">
            <strong>Email:</strong> {{ trainer.email }}
          </p>
          <p v-if="trainer.phone">
            <strong>Телефон:</strong> {{ trainer.phone }}
          </p>
        </div>
        
        <div class="trainer-stats">
          <div class="stat">
            <span class="stat-value">{{ trainer.workouts_count || 0 }}</span>
            <span class="stat-label">Тренировок</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ trainer.average_rating?.toFixed(1) || '0.0' }}</span>
            <span class="stat-label">Рейтинг</span>
          </div>
        </div>
        
        <div class="trainer-actions">
          <button @click="viewTrainerSchedule(trainer.id)" class="btn btn-secondary">
            Расписание
          </button>
          <button @click="viewTrainerDetails(trainer.id)" class="btn btn-primary">
            Подробнее
          </button>
          <button 
            v-if="isAuthenticated && !isEmployee"
            @click="leaveFeedback(trainer.id)"
            class="btn btn-warning"
          >
            Оставить отзыв
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { fitnessAPI } from '../../services/api'
import { useAuthStore } from '../../store/auth'

export default {
  name: 'Trainers',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const trainers = ref([])
    const specializations = ref([])
    const isLoading = ref(false)
    
    const filters = ref({
      specializationId: '',
      minExperience: ''
    })
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const isEmployee = computed(() => authStore.isEmployee)
    
    const fetchData = async () => {
      isLoading.value = true
      try {
        const [trainersRes] = await Promise.all([
          fitnessAPI.getTrainers(),
        ])
        
        trainers.value = trainersRes.data
        
        // Получаем уникальные специализации
        const uniqueSpecs = new Map()
        trainers.value.forEach(trainer => {
          if (trainer.specialization) {
            uniqueSpecs.set(trainer.specialization.id, trainer.specialization)
          }
        })
        specializations.value = Array.from(uniqueSpecs.values())
      } catch (error) {
        console.error('Error fetching trainers:', error)
      } finally {
        isLoading.value = false
      }
    }
    
    const filteredTrainers = computed(() => {
      let result = trainers.value
      
      if (filters.value.specializationId) {
        result = result.filter(trainer => 
          trainer.specialization?.id === parseInt(filters.value.specializationId)
        )
      }
      
      if (filters.value.minExperience) {
        result = result.filter(trainer => 
          trainer.work_experience >= parseInt(filters.value.minExperience)
        )
      }
      
      return result
    })
    
    const applyFilters = () => {
      // Фильтры применяются через computed свойство
    }
    
    const resetFilters = () => {
      filters.value = {
        specializationId: '',
        minExperience: ''
      }
    }
    
    const viewTrainerSchedule = (trainerId) => {
      router.push({
        path: '/schedule',
        query: { trainerId }
      })
    }
    
    const viewTrainerDetails = (trainerId) => {
      router.push(`/trainers/${trainerId}`)
    }
    
    const leaveFeedback = (trainerId) => {
      router.push(`/feedback/${trainerId}`)
    }
    
    onMounted(() => {
      fetchData()
    })
    
    return {
      trainers,
      specializations,
      isLoading,
      filters,
      isAuthenticated,
      isEmployee,
      filteredTrainers,
      applyFilters,
      resetFilters,
      viewTrainerSchedule,
      viewTrainerDetails,
      leaveFeedback
    }
  }
}
</script>

<style scoped>
.trainers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 30px;
  margin-top: 30px;
}

.trainer-card {
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
}

.trainer-card:hover {
  transform: translateY(-5px);
}

.trainer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
}

.trainer-header h3 {
  color: var(--accent-orange);
  margin: 0;
}

.specialization {
  background: linear-gradient(135deg, var(--accent-orange), var(--accent-purple));
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
}

.trainer-info {
  flex: 1;
  margin-bottom: 20px;
}

.trainer-info p {
  margin: 8px 0;
  color: var(--text-muted);
}

.trainer-info strong {
  color: var(--text-light);
}

.trainer-stats {
  display: flex;
  gap: 20px;
  margin: 15px 0;
  padding: 15px;
  background-color: var(--primary-dark);
  border-radius: var(--radius);
}

.stat {
  text-align: center;
  flex: 1;
}

.stat-value {
  display: block;
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--accent-orange);
  margin-bottom: 5px;
}

.stat-label {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.trainer-actions {
  display: flex;
  gap: 10px;
  margin-top: auto;
}

.filters {
  margin-bottom: 30px;
}

.filters .row {
  margin-bottom: 15px;
}

.filters button {
  margin-right: 10px;
}
</style>