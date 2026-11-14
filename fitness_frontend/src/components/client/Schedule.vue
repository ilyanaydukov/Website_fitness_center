<template>
  <div class="container">
    <h1 class="page-title">Расписание тренировок</h1>
    
    <div class="filters card">
      <div class="row">
        <div class="col">
          <label class="form-label">Дата от:</label>
          <input type="date" v-model="filters.dateFrom" class="form-control" />
        </div>
        <div class="col">
          <label class="form-label">Дата до:</label>
          <input type="date" v-model="filters.dateTo" class="form-control" />
        </div>
        <div class="col">
          <label class="form-label">Тренер:</label>
          <select v-model="filters.trainerId" class="form-control">
            <option value="">Все тренеры</option>
            <option v-for="trainer in trainers" :key="trainer.id" :value="trainer.id">
              {{ trainer.first_name }} {{ trainer.last_name }}
            </option>
          </select>
        </div>
        <div class="col">
          <label class="form-label">Услуга:</label>
          <select v-model="filters.serviceId" class="form-control">
            <option value="">Все услуги</option>
            <option v-for="service in services" :key="service.id" :value="service.id">
              {{ service.name }}
            </option>
          </select>
        </div>
      </div>
      <button @click="applyFilters" class="btn btn-primary" :disabled="isLoading">
        Применить
      </button>
      <button @click="resetFilters" class="btn btn-secondary">
        Сбросить
      </button>
    </div>
    
    <div v-if="isLoading" class="loader"></div>
    
    <div v-else>
      <div v-if="workouts.length === 0" class="alert alert-warning">
        Нет доступных тренировок
      </div>
      
      <div v-else class="grid">
        <div v-for="workout in workouts" :key="workout.id" class="card workout-card">
          <div class="workout-header">
            <h3>{{ workout.service?.name || 'Тренировка' }}</h3>
            <span class="badge" :class="getCapacityClass(workout)">
              {{ workout.current_number_of_recorded }}/{{ workout.max_persons_capacity }}
            </span>
          </div>
          
          <div class="workout-details">
            <p><strong>Дата:</strong> {{ formatDate(workout.workout_date) }}</p>
            <p><strong>Время:</strong> {{ workout.start_time }} - {{ workout.end_time }}</p>
            <p><strong>Тренер:</strong> {{ workout.trainer?.first_name }} {{ workout.trainer?.last_name }}</p>
            <p><strong>Зал:</strong> {{ workout.room?.name }}</p>
            <p><strong>Описание:</strong> {{ workout.service?.description || 'Нет описания' }}</p>
          </div>
          
          <div class="workout-actions">
            <button 
              @click="viewDetails(workout.id)"
              class="btn btn-secondary"
            >
              Подробнее
            </button>
            
            <button 
              v-if="isAuthenticated && !isEmployee"
              @click="registerForWorkout(workout.id)"
              class="btn btn-primary"
              :disabled="workout.current_number_of_recorded >= workout.max_persons_capacity"
            >
              {{ workout.current_number_of_recorded >= workout.max_persons_capacity ? 'Мест нет' : 'Записаться' }}
            </button>
            
            <button 
              v-if="isEmployee"
              @click="editWorkout(workout.id)"
              class="btn btn-warning"
            >
              Редактировать
            </button>
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
  name: 'Schedule',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const workouts = ref([])
    const trainers = ref([])
    const services = ref([])
    const isLoading = ref(false)
    
    const filters = ref({
      dateFrom: '',
      dateTo: '',
      trainerId: '',
      serviceId: ''
    })
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const isEmployee = computed(() => authStore.isEmployee)
    
    const fetchData = async () => {
      isLoading.value = true
      try {
        const [workoutsRes, trainersRes, servicesRes] = await Promise.all([
          fitnessAPI.getWorkouts(filters.value),
          fitnessAPI.getTrainers(),
          fitnessAPI.getServices()
        ])
        
        workouts.value = workoutsRes.data
        trainers.value = trainersRes.data
        services.value = servicesRes.data
      } catch (error) {
        console.error('Error fetching data:', error)
      } finally {
        isLoading.value = false
      }
    }
    
    const applyFilters = () => {
      fetchData()
    }
    
    const resetFilters = () => {
      filters.value = {
        dateFrom: '',
        dateTo: '',
        trainerId: '',
        serviceId: ''
      }
      fetchData()
    }
    
    const formatDate = (dateString) => {
      return format(new Date(dateString), 'dd.MM.yyyy')
    }
    
    const getCapacityClass = (workout) => {
      if (workout.current_number_of_recorded >= workout.max_persons_capacity) {
        return 'badge-danger'
      } else if (workout.current_number_of_recorded >= workout.max_persons_capacity * 0.8) {
        return 'badge-warning'
      }
      return 'badge-success'
    }
    
    const viewDetails = (id) => {
      router.push(`/workout/${id}`)
    }
    
    const registerForWorkout = async (id) => {
      try {
        await fitnessAPI.registerForWorkout(id)
        alert('Вы успешно записались на тренировку!')
        fetchData()
      } catch (error) {
        alert(error.response?.data?.detail || 'Ошибка записи')
      }
    }
    
    const editWorkout = (id) => {
      router.push(`/admin/workouts/edit/${id}`)
    }
    
    onMounted(() => {
      fetchData()
    })
    
    return {
      workouts,
      trainers,
      services,
      isLoading,
      filters,
      isAuthenticated,
      isEmployee,
      applyFilters,
      resetFilters,
      formatDate,
      getCapacityClass,
      viewDetails,
      registerForWorkout,
      editWorkout
    }
  }
}
</script>

<style scoped>
.workout-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  transition: transform 0.3s ease;
}

.workout-card:hover {
  transform: translateY(-5px);
}

.workout-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.workout-header h3 {
  margin: 0;
  color: var(--accent-orange);
}

.workout-details {
  flex: 1;
  margin-bottom: 15px;
}

.workout-details p {
  margin: 5px 0;
}

.workout-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
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