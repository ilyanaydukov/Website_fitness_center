<template>
  <div class="container">
    <div class="admin-header">
      <h1 class="page-title">Управление тренерами</h1>
      <button @click="showCreateModal = true" class="btn btn-primary">
        + Добавить тренера
      </button>
    </div>
    
    <div v-if="isLoading" class="loader"></div>
    
    <div v-else>
      <div class="search-filter">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Поиск по имени, email или специализации..."
          class="form-control"
          @input="debouncedSearch"
        />
      </div>
      
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>ФИО</th>
            <th>Email</th>
            <th>Специализация</th>
            <th>Опыт</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="trainer in filteredTrainers" :key="trainer.id">
            <td>{{ trainer.id }}</td>
            <td>{{ trainer.first_name }} {{ trainer.last_name }}</td>
            <td>{{ trainer.email }}</td>
            <td>
              <span v-if="trainer.specialization" class="badge bg-primary">
                {{ trainer.specialization.name }}
              </span>
              <span v-else class="text-muted">Не указана</span>
            </td>
            <td>{{ trainer.work_experience || '0' }} лет</td>
            <td>
              <button @click="editTrainer(trainer)" class="btn btn-sm btn-secondary me-2">
                Редактировать
              </button>
              <button @click="deleteTrainer(trainer.id)" class="btn btn-sm btn-danger me-2">
                Удалить
              </button>
              <button @click="viewFeedbacks(trainer.id)" class="btn btn-sm btn-primary">
                Отзывы ({{ trainer.feedbacks?.length || 0 }})
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="filteredTrainers.length === 0" class="empty-state">
        <p>{{ searchQuery ? 'Тренеры не найдены по запросу' : 'Тренеры не найдены' }}</p>
      </div>
    </div>
    
    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editingTrainer ? 'Редактировать' : 'Добавить' }} тренера</h3>
          <button @click="closeModal" class="btn btn-sm btn-danger">&times;</button>
        </div>
        
        <form @submit.prevent="saveTrainer" class="modal-form">
          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Имя *</label>
              <input type="text" v-model="trainerForm.first_name" required class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Фамилия *</label>
              <input type="text" v-model="trainerForm.last_name" required class="form-control" />
            </div>
          </div>
          
          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Email *</label>
              <input type="email" v-model="trainerForm.email" required class="form-control" 
                     :readonly="!!editingTrainer" />
              <small v-if="editingTrainer" class="text-muted">
                Email нельзя изменить после создания
              </small>
            </div>
            <div class="col-md-6">
              <label class="form-label">Пароль {{ editingTrainer ? '(оставьте пустым для сохранения текущего)' : '*' }}</label>
              <input type="password" v-model="trainerForm.password" 
                     :required="!editingTrainer" class="form-control" />
            </div>
          </div>
          
          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Специализация</label>
              <select v-model="trainerForm.specialization_id" class="form-control">
                <option value="">Выберите специализацию</option>
                <option v-for="spec in specializations" :key="spec.id" :value="spec.id">
                  {{ spec.name }}
                </option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label">Опыт работы (лет)</label>
              <input type="number" v-model="trainerForm.work_experience" class="form-control" min="0" max="50" />
            </div>
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
    
    <!-- Feedbacks Modal -->
    <div v-if="showFeedbacksModal" class="modal-overlay">
      <div class="modal modal-lg">
        <div class="modal-header">
          <h3>Отзывы о тренере {{ selectedTrainerName }}</h3>
          <button @click="closeFeedbacksModal" class="btn btn-sm btn-danger">&times;</button>
        </div>
        
        <div class="modal-body">
          <div v-if="selectedTrainerFeedbacks.length === 0" class="empty-state">
            <p>Нет отзывов</p>
          </div>
          
          <div v-else class="feedbacks-list">
            <div v-for="feedback in selectedTrainerFeedbacks" :key="feedback.id" class="feedback-item card mb-3">
              <div class="card-body">
                <div class="feedback-header d-flex justify-content-between align-items-center mb-3">
                  <div class="feedback-rating d-flex align-items-center">
                    <div class="stars me-2">
                      <span v-for="star in 5" :key="star" 
                            class="star" :class="{ 'active': star <= feedback.mark }">
                        ★
                      </span>
                    </div>
                    <span class="rating-value fw-bold">{{ feedback.mark }}/5</span>
                  </div>
                  <span class="feedback-date text-muted">{{ formatDate(feedback.feedback_date) }}</span>
                </div>
                
                <div class="feedback-comment mb-3">
                  <p class="mb-0">{{ feedback.comment || 'Без комментария' }}</p>
                </div>
                
                <div class="feedback-client text-end">
                  <small class="text-muted">
                    Клиент: {{ feedback.client?.first_name }} {{ feedback.client?.last_name }}
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="closeFeedbacksModal" class="btn btn-secondary">Закрыть</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { format } from 'date-fns'
import { fitnessAPI } from '../../services/api'

export default {
  name: 'TrainerManagement',
  setup() {
    const trainers = ref([])
    const specializations = ref([])
    const selectedTrainerFeedbacks = ref([])
    const selectedTrainerName = ref('')
    const isLoading = ref(false)
    const isSaving = ref(false)
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const showFeedbacksModal = ref(false)
    const editingTrainer = ref(null)
    const searchQuery = ref('')
    let searchTimeout = null
    
    const trainerForm = ref({
      first_name: '',
      last_name: '',
      specialization_id: '',
      work_experience: 0,
      email: '',
      password: ''
    })
    
    const filteredTrainers = computed(() => {
      if (!searchQuery.value.trim()) return trainers.value
      
      const query = searchQuery.value.toLowerCase().trim()
      return trainers.value.filter(trainer => {
        const fullName = `${trainer.first_name} ${trainer.last_name}`.toLowerCase()
        const specializationName = trainer.specialization?.name?.toLowerCase() || ''
        
        return fullName.includes(query) ||
               trainer.email?.toLowerCase().includes(query) ||
               specializationName.includes(query)
      })
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
        console.log('Загрузка данных о тренерах...')
        
        const trainersRes = await fitnessAPI.getAdminTrainers()
        trainers.value = trainersRes.data || []
        
        console.log('Данные тренеров загружены:', trainers.value.length)
        
      } catch (error) {
        console.error('Ошибка при загрузке данных тренеров:', error)
        
        // Резервный план: используем публичный API
        try {
          const backupRes = await fitnessAPI.getTrainers()
          trainers.value = backupRes.data || []
        } catch (backupError) {
          console.error('Ошибка резервной загрузки:', backupError)
          alert('Не удалось загрузить данные тренеров. Проверьте подключение к серверу.')
        }
      } finally {
        isLoading.value = false
      }
    }
    
    // ДОБАВЛЕНО: Функция для загрузки специализаций
    const fetchSpecializations = async () => {
      try {
        const response = await fitnessAPI.getSpecializations()
        specializations.value = response.data || []
        console.log('Специализации загружены:', specializations.value.length)
      } catch (error) {
        console.error('Error fetching specializations:', error)
        // Заглушка на случай ошибки
        specializations.value = [
          { id: 1, name: 'Фитнес', description: 'Общая физическая подготовка' },
          { id: 2, name: 'Йога', description: 'Йога и стретчинг' },
          { id: 3, name: 'Кардио', description: 'Кардиотренировки' },
          { id: 4, name: 'Силовые тренировки', description: 'Тяжелая атлетика, пауэрлифтинг' },
          { id: 5, name: 'Пилатес', description: 'Пилатес и функциональный тренинг' },
          { id: 6, name: 'CrossFit', description: 'Кроссфит и функциональный тренинг' }
        ]
        console.log('Используются временные данные специализаций')
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      try {
        return format(new Date(dateString), 'dd.MM.yyyy HH:mm')
      } catch (e) {
        return dateString
      }
    }
    
    const editTrainer = (trainer) => {
      editingTrainer.value = trainer
      trainerForm.value = { 
        first_name: trainer.first_name || '',
        last_name: trainer.last_name || '',
        specialization_id: trainer.specialization_id || '',
        work_experience: trainer.work_experience || 0,
        email: trainer.email || '',
        password: '' // Оставляем пустым для редактирования
      }
      showEditModal.value = true
    }
    
    const deleteTrainer = async (id) => {
      if (!confirm('Вы уверены, что хотите удалить этого тренера? Все связанные данные будут удалены.')) return
      
      try {
        await fitnessAPI.deleteTrainer(id)
        alert('Тренер удален успешно!')
        fetchData()
      } catch (error) {
        console.error('Delete error:', error)
        alert('Ошибка при удалении тренера: ' + (error.response?.data?.detail || error.message))
      }
    }
    
    const saveTrainer = async () => {
      isSaving.value = true
      try {
        // Подготовить данные для отправки
        const trainerData = {
          first_name: trainerForm.value.first_name.trim(),
          last_name: trainerForm.value.last_name.trim(),
          specialization_id: parseInt(trainerForm.value.specialization_id) || null,
          work_experience: parseInt(trainerForm.value.work_experience) || 0,
          email: trainerForm.value.email.trim()
        }
        
        // Добавить пароль только если он указан
        if (trainerForm.value.password.trim()) {
          trainerData.password = trainerForm.value.password
        }
        
        console.log('Saving trainer data:', trainerData)
        
        if (editingTrainer.value) {
          // Для обновления отправляем в /admin/trainers/{id}
          await fitnessAPI.updateTrainer(editingTrainer.value.id, trainerData)
          alert('Тренер обновлен успешно!')
        } else {
          // Для создания отправляем в /admin/trainers
          // Проверить обязательные поля для создания
          if (!trainerData.password) {
            throw new Error('Пароль обязателен для нового тренера')
          }
          await fitnessAPI.createTrainer(trainerData)
          alert('Тренер создан успешно!')
        }
        
        closeModal()
        fetchData()
      } catch (error) {
        console.error('Save trainer error:', error)
        
        // Более детальное сообщение об ошибке
        let errorMessage = 'Неизвестная ошибка'
        if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message
        } else if (error.message) {
          errorMessage = error.message
        }
        
        alert('Ошибка сохранения: ' + errorMessage)
      } finally {
        isSaving.value = false
      }
    }
    
    const viewFeedbacks = async (trainerId) => {
      try {
        const trainer = trainers.value.find(t => t.id === trainerId)
        if (trainer) {
          selectedTrainerName.value = `${trainer.first_name} ${trainer.last_name}`
        }
        
        const response = await fitnessAPI.getTrainerFeedbacks(trainerId)
        selectedTrainerFeedbacks.value = response.data
        showFeedbacksModal.value = true
      } catch (error) {
        console.error('Error fetching feedbacks:', error)
        alert('Ошибка при загрузке отзывов')
      }
    }
    
    const closeModal = () => {
      showCreateModal.value = false
      showEditModal.value = false
      editingTrainer.value = null
      trainerForm.value = {
        first_name: '',
        last_name: '',
        specialization_id: '',
        work_experience: 0,
        email: '',
        password: ''
      }
    }
    
    const closeFeedbacksModal = () => {
      showFeedbacksModal.value = false
      selectedTrainerFeedbacks.value = []
      selectedTrainerName.value = ''
    }
    
    // ИСПРАВЛЕНО: Обновленный onMounted с вызовом обеих функций
    onMounted(() => {
      fetchData()
      fetchSpecializations() // Добавлен вызов функции загрузки специализаций
    })
    
    return {
      trainers,
      specializations,
      selectedTrainerFeedbacks,
      selectedTrainerName,
      isLoading,
      isSaving,
      showCreateModal,
      showEditModal,
      showFeedbacksModal,
      editingTrainer,
      searchQuery,
      filteredTrainers,
      trainerForm,
      fetchData,
      formatDate,
      editTrainer,
      deleteTrainer,
      saveTrainer,
      viewFeedbacks,
      closeModal,
      closeFeedbacksModal,
      debouncedSearch
    }
  }
}
</script>

<style scoped>
.search-filter {
  margin-bottom: 20px;
  max-width: 400px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--text-muted);
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

.modal.modal-lg {
  max-width: 800px;
}

.feedbacks-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.feedback-item {
  padding: 15px;
  background-color: var(--primary-dark);
  border-radius: var(--radius);
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.feedback-rating {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stars .star {
  font-size: 1.2rem;
  color: var(--border-color);
}

.stars .star.active {
  color: gold;
}

.rating-value {
  font-weight: 600;
  color: var(--accent-orange);
}

.feedback-date {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.feedback-comment {
  color: var(--text-muted);
  line-height: 1.5;
  margin-bottom: 10px;
  font-style: italic;
}

.feedback-client {
  color: var(--text-light);
  font-size: 0.9rem;
  font-weight: 500;
}

.badge {
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
}
</style>