<template>
  <div class="container">
    <h1 class="page-title">Генерация отчетов</h1>
    
    <div class="grid">
      <!-- Equipment Report -->
      <div class="card">
        <div class="card-header">
          <h3>Отчет по оборудованию</h3>
          <p class="card-subtitle">PDF с информацией об инвентаре</p>
        </div>
        <div class="card-body">
          <button @click="generateEquipmentReport" class="btn btn-primary" :disabled="isGenerating">
            Сгенерировать отчет
          </button>
        </div>
      </div>
      
      <!-- Schedule Report -->
      <div class="card">
        <div class="card-header">
          <h3>Отчет по расписанию</h3>
          <p class="card-subtitle">PDF с расписанием за период</p>
        </div>
        <div class="card-body">
          <div class="form-group">
            <label class="form-label">Дата от:</label>
            <input type="date" v-model="scheduleDateFrom" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Дата до:</label>
            <input type="date" v-model="scheduleDateTo" class="form-control" />
          </div>
          <button @click="generateScheduleReport" class="btn btn-primary" :disabled="isGenerating">
            Сгенерировать отчет
          </button>
        </div>
      </div>
      
      <!-- Registrations Report -->
      <div class="card">
        <div class="card-header">
          <h3>Отчет по записям</h3>
          <p class="card-subtitle">PDF с записавшимися на тренировку</p>
        </div>
        <div class="card-body">
          <div class="form-group">
            <label class="form-label">Тренировка</label>
            <select v-model="selectedWorkoutId" class="form-control">
              <option value="">Выберите тренировку</option>
              <option v-for="workout in workouts" :key="workout.id" :value="workout.id">
                {{ formatWorkoutInfo(workout) }}
              </option>
            </select>
          </div>
          <button 
            @click="generateRegistrationsReport" 
            class="btn btn-primary" 
            :disabled="isGenerating || !selectedWorkoutId"
          >
            Сгенерировать отчет
          </button>
        </div>
      </div>
    </div>
    
    <div v-if="isGenerating" class="loader"></div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { format } from 'date-fns'
import { fitnessAPI } from '../../services/api'

export default {
  name: 'ReportGeneration',
  setup() {
    const isGenerating = ref(false)
    const workouts = ref([])
    const scheduleDateFrom = ref('')
    const scheduleDateTo = ref('')
    const selectedWorkoutId = ref('')
    
    const fetchWorkouts = async () => {
      try {
        const response = await fitnessAPI.getWorkouts()
        workouts.value = response.data
      } catch (error) {
        console.error('Error fetching workouts:', error)
      }
    }
    
    const generateEquipmentReport = async () => {
      isGenerating.value = true
      try {
        const response = await fitnessAPI.generateEquipmentPDF()
        downloadPDF(response.data, 'equipment_report.pdf')
      } catch (error) {
        alert('Ошибка при генерации отчета')
      } finally {
        isGenerating.value = false
      }
    }
    
    const generateScheduleReport = async () => {
      if (!scheduleDateFrom.value || !scheduleDateTo.value) {
        alert('Пожалуйста, выберите период')
        return
      }
      
      isGenerating.value = true
      try {
        const response = await fitnessAPI.generateSchedulePDF(
          scheduleDateFrom.value,
          scheduleDateTo.value
        )
        downloadPDF(response.data, 'schedule_report.pdf')
      } catch (error) {
        alert('Ошибка при генерации отчета')
      } finally {
        isGenerating.value = false
      }
    }
    
    const generateRegistrationsReport = async () => {
      if (!selectedWorkoutId.value) {
        alert('Пожалуйста, выберите тренировку')
        return
      }
      
      isGenerating.value = true
      try {
        const response = await fitnessAPI.generateRegistrationsPDF(selectedWorkoutId.value)
        downloadPDF(response.data, `registrations_${selectedWorkoutId.value}.pdf`)
      } catch (error) {
        alert('Ошибка при генерации отчета')
      } finally {
        isGenerating.value = false
      }
    }
    
    const downloadPDF = (blob, filename) => {
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    }
    
    const formatWorkoutInfo = (workout) => {
      return `${workout.service?.name} - ${format(new Date(workout.workout_date), 'dd.MM.yyyy')}`
    }
    
    onMounted(() => {
      fetchWorkouts()
    })
    
    return {
      isGenerating,
      workouts,
      scheduleDateFrom,
      scheduleDateTo,
      selectedWorkoutId,
      generateEquipmentReport,
      generateScheduleReport,
      generateRegistrationsReport,
      formatWorkoutInfo
    }
  }
}
</script>

<style scoped>
.card {
  height: 100%;
}

.card-body {
  padding: 20px 0;
}

.card-body .btn {
  margin-top: 10px;
}

.grid {
  margin-top: 30px;
}

.form-group {
  margin-bottom: 15px;
}
</style>