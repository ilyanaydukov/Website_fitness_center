<template>
  <div class="container">
    <div class="admin-header">
      <h1 class="page-title">Управление тренировками</h1>
      <button @click="showCreateModal = true" class="btn btn-primary">
        + Создать тренировку
      </button>
    </div>
    
    <div v-if="isLoading" class="loader"></div>
    
    <div v-else>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Дата</th>
            <th>Время</th>
            <th>Услуга</th>
            <th>Тренер</th>
            <th>Зал</th>
            <th>Записано</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="workout in workouts" :key="workout.id">
            <td>{{ workout.id }}</td>
            <td>{{ formatDate(workout.workout_date) }}</td>
            <td>{{ workout.start_time }} - {{ workout.end_time }}</td>
            <td>{{ workout.service?.name }}</td>
            <td>
              <span v-if="workout.trainer">
                {{ workout.trainer.first_name }} {{ workout.trainer.last_name }}
              </span>
              <span v-else class="text-muted">Не назначен</span>
            </td>
            <td>{{ workout.room?.name }}</td>
            <td>{{ workout.current_number_of_recorded || 0 }}/{{ workout.max_persons_capacity }}</td>
            <td>
              <button @click="editWorkout(workout)" class="btn btn-sm btn-secondary">
                Редактировать
              </button>
              <button @click="deleteWorkout(workout.id)" class="btn btn-sm btn-danger">
                Удалить
              </button>
              <button @click="viewRegistrations(workout.id)" class="btn btn-sm btn-primary">
                Записи
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editingWorkout ? 'Редактировать' : 'Создать' }} тренировку</h3>
          <button @click="closeModal" class="btn btn-sm btn-danger">&times;</button>
        </div>
        
        <form @submit.prevent="saveWorkout" class="modal-form">
          <div class="row">
            <div class="col">
              <label class="form-label">Дата *</label>
              <input type="date" v-model="workoutForm.workout_date" required class="form-control" />
            </div>
            <div class="col">
              <label class="form-label">Время начала *</label>
              <input type="time" v-model="workoutForm.start_time" required class="form-control" />
            </div>
            <div class="col">
              <label class="form-label">Время окончания *</label>
              <input type="time" v-model="workoutForm.end_time" required class="form-control" />
            </div>
          </div>
          
          <div class="row">
            <div class="col">
              <label class="form-label">Услуга *</label>
              <select v-model="workoutForm.service_id" required class="form-control">
                <option value="">Выберите услугу</option>
                <option v-for="service in services" :key="service.id" :value="service.id">
                  {{ service.name }}
                </option>
              </select>
            </div>
            <div class="col">
              <label class="form-label">Тренер *</label>
              <select v-model="workoutForm.trainer_id" required class="form-control">
                <option value="">Выберите тренера</option>
                <option v-for="trainer in trainers" :key="trainer.id" :value="trainer.id">
                  {{ trainer.first_name }} {{ trainer.last_name }}
                  <span v-if="trainer.specialization">
                    ({{ trainer.specialization.name }})
                  </span>
                </option>
              </select>
              <div v-if="trainers.length === 0" class="alert alert-warning mt-2">
                Нет доступных тренеров. Сначала создайте тренеров в системе.
              </div>
            </div>
          </div>
          
          <div class="row">
            <div class="col">
              <label class="form-label">Зал *</label>
              <select v-model="workoutForm.room_id" required class="form-control">
                <option value="">Выберите зал</option>
                <option v-for="room in rooms" :key="room.id" :value="room.id">
                  {{ room.name }} (Центр: {{ room.fitness_center?.name }})
                </option>
              </select>
            </div>
            <div class="col">
              <label class="form-label">Максимальное количество человек *</label>
              <input type="number" v-model="workoutForm.max_persons_capacity" required class="form-control" min="1" />
            </div>
          </div>
          
          <div v-if="errorMessage" class="alert alert-danger mt-3">
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
import { format } from 'date-fns'
import { fitnessAPI } from '../../services/api'

export default {
  name: 'WorkoutManagement',
  setup() {
    const workouts = ref([])
    const services = ref([])
    const trainers = ref([])
    const rooms = ref([])
    const isLoading = ref(false)
    const isSaving = ref(false)
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const editingWorkout = ref(null)
    const errorMessage = ref('')
    
    const workoutForm = ref({
      workout_date: '',
      start_time: '',
      end_time: '',
      service_id: '',
      trainer_id: '',
      room_id: '',
      max_persons_capacity: 10,
      current_number_of_recorded: 0
    })
    
    const fetchData = async () => {
      isLoading.value = true
      try {
        console.log('Начало загрузки данных...')
        
        // Загружаем все данные параллельно
        const [workoutsRes, servicesRes, roomsRes] = await Promise.all([
          fitnessAPI.getWorkouts(),
          fitnessAPI.getServices(),
          fitnessAPI.getRooms()
        ])
        
        workouts.value = workoutsRes.data || []
        services.value = servicesRes.data || []
        rooms.value = roomsRes.data || []
        
        console.log('Тренировки загружены:', workouts.value.length)
        console.log('Услуги загружены:', services.value.length)
        console.log('Залы загружены:', rooms.value.length)
        
        // Отдельно загружаем тренеров
        await fetchTrainers()
        
      } catch (error) {
        console.error('Error fetching data:', error)
        errorMessage.value = 'Ошибка при загрузке данных: ' + (error.message || 'Неизвестная ошибка')
      } finally {
        isLoading.value = false
      }
    }
    
    const fetchTrainers = async () => {
      try {
        console.log('Пытаемся загрузить тренеров...')
        
        // Пробуем несколько эндпоинтов
        let trainersData = []
        
        // 1. Пробуем админский эндпоинт
        try {
          const adminResponse = await fitnessAPI.getAdminTrainers()
          if (adminResponse.data && Array.isArray(adminResponse.data)) {
            trainersData = adminResponse.data
            console.log('Тренеры загружены из админского эндпоинта:', trainersData.length)
          }
        } catch (adminError) {
          console.log('Админский эндпоинт не сработал:', adminError.message)
        }
        
        // 2. Если нет данных, пробуем публичный эндпоинт
        if (trainersData.length === 0) {
          try {
            const publicResponse = await fitnessAPI.getTrainers()
            if (publicResponse.data && Array.isArray(publicResponse.data)) {
              trainersData = publicResponse.data
              console.log('Тренеры загружены из публичного эндпоинта:', trainersData.length)
            }
          } catch (publicError) {
            console.log('Публичный эндпоинт не сработал:', publicError.message)
          }
        }
        
        // 3. Если все еще нет данных, пробуем прямой запрос к API
        if (trainersData.length === 0) {
          try {
            const directResponse = await api.get('/fitness/trainers?limit=100')
            if (directResponse.data && Array.isArray(directResponse.data)) {
              trainersData = directResponse.data
              console.log('Тренеры загружены прямым запросом:', trainersData.length)
            }
          } catch (directError) {
            console.log('Прямой запрос не сработал:', directError.message)
          }
        }
        
        // 4. Преобразуем данные тренеров в нужный формат
        trainers.value = trainersData.map(trainer => {
          // Если тренер имеет вложенную структуру (employee внутри)
          if (trainer.employee) {
            return {
              id: trainer.id,
              first_name: trainer.employee.first_name || trainer.first_name || '',
              last_name: trainer.employee.last_name || trainer.last_name || '',
              specialization: trainer.specialization || null,
              email: trainer.employee.email || trainer.email || '',
              phone: trainer.employee.phone || trainer.phone || '',
              work_experience: trainer.work_experience || 0
            }
          }
          
          // Если тренер имеет плоскую структуру
          return {
            id: trainer.id,
            first_name: trainer.first_name || '',
            last_name: trainer.last_name || '',
            specialization: trainer.specialization || null,
            email: trainer.email || '',
            phone: trainer.phone || '',
            work_experience: trainer.work_experience || 0
          }
        }).filter(trainer => trainer.first_name && trainer.last_name) // Фильтруем только валидных тренеров
        
        console.log('Обработанные тренеры:', trainers.value)
        
        if (trainers.value.length === 0) {
          console.warn('Нет данных о тренерах. Проверьте подключение к базе данных.')
        }
        
      } catch (error) {
        console.error('Error fetching trainers:', error)
        trainers.value = []
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      try {
        return format(new Date(dateString), 'dd.MM.yyyy')
      } catch (e) {
        return dateString
      }
    }
    
    const editWorkout = (workout) => {
      editingWorkout.value = workout
      workoutForm.value = { 
        workout_date: workout.workout_date ? workout.workout_date.split('T')[0] : '',
        start_time: workout.start_time || '',
        end_time: workout.end_time || '',
        service_id: workout.service_id || '',
        trainer_id: workout.trainer_id || '',
        room_id: workout.room_id || '',
        max_persons_capacity: workout.max_persons_capacity || 10,
        current_number_of_recorded: workout.current_number_of_recorded || 0
      }
      showEditModal.value = true
      errorMessage.value = ''
    }
    
    const deleteWorkout = async (id) => {
      if (!confirm('Вы уверены, что хотите удалить эту тренировку? Все записи на неё будут удалены.')) return
      
      try {
        await fitnessAPI.deleteWorkout(id)
        alert('Тренировка удалена успешно!')
        fetchData()
      } catch (error) {
        console.error('Delete error:', error)
        alert('Ошибка при удалении тренировки: ' + (error.response?.data?.detail || error.message))
      }
    }
    
    const saveWorkout = async () => {
      isSaving.value = true
      errorMessage.value = ''
      
      try {
        // Валидация
        if (!workoutForm.value.trainer_id) {
          throw new Error('Выберите тренера')
        }
        
        if (!workoutForm.value.service_id) {
          throw new Error('Выберите услугу')
        }
        
        if (!workoutForm.value.room_id) {
          throw new Error('Выберите зал')
        }
        
        // Проверяем, что выбранный тренер существует
        const selectedTrainer = trainers.value.find(
          trainer => trainer.id === parseInt(workoutForm.value.trainer_id)
        )
        
        if (!selectedTrainer) {
          throw new Error('Выбранный тренер не существует')
        }
        
        // Подготовить данные для отправки
        const workoutData = {
          workout_date: workoutForm.value.workout_date,
          start_time: workoutForm.value.start_time,
          end_time: workoutForm.value.end_time,
          service_id: parseInt(workoutForm.value.service_id),
          trainer_id: parseInt(workoutForm.value.trainer_id),
          room_id: parseInt(workoutForm.value.room_id),
          max_persons_capacity: parseInt(workoutForm.value.max_persons_capacity) || 10,
          current_number_of_recorded: parseInt(workoutForm.value.current_number_of_recorded) || 0
        }
        
        console.log('Saving workout data:', workoutData)
        
        if (editingWorkout.value) {
          await fitnessAPI.updateWorkout(editingWorkout.value.id, workoutData)
          alert('Тренировка обновлена успешно!')
        } else {
          await fitnessAPI.createWorkout(workoutData)
          alert('Тренировка создана успешно!')
        }
        
        closeModal()
        fetchData()
      } catch (error) {
        console.error('Save workout error:', error)
        
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
      editingWorkout.value = null
      workoutForm.value = {
        workout_date: '',
        start_time: '',
        end_time: '',
        service_id: '',
        trainer_id: '',
        room_id: '',
        max_persons_capacity: 10,
        current_number_of_recorded: 0
      }
      errorMessage.value = ''
    }
    
    const viewRegistrations = async (workoutId) => {
      try {
        alert(`Просмотр записей на тренировку ${workoutId}. Функционал в разработке.`)
      } catch (error) {
        console.error('View registrations error:', error)
      }
    }
    
    onMounted(() => {
      fetchData()
    })
    
    return {
      workouts,
      services,
      trainers,
      rooms,
      isLoading,
      isSaving,
      showCreateModal,
      showEditModal,
      editingWorkout,
      workoutForm,
      errorMessage,
      fetchData,
      formatDate,
      editWorkout,
      deleteWorkout,
      saveWorkout,
      closeModal,
      viewRegistrations
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
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  margin: 0;
  color: var(--accent-orange);
}

.modal-form .row {
  margin-bottom: 15px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.table {
  margin-top: 20px;
}

.table button {
  margin-right: 5px;
}
</style>