<template>
  <div class="container">
    <h1 class="page-title">Фитнес-центры</h1>
    
    <div v-if="isLoading" class="loader"></div>
    
    <div v-else class="centers-grid">
      <div v-for="center in centers" :key="center.id" class="card center-card">
        <div class="center-image">
          <div class="image-placeholder">🏋️‍♂️</div>
        </div>
        
        <div class="center-content">
          <h3 class="center-title">{{ center.name }}</h3>
          
          <div class="center-info">
            <p><strong>📍 Адрес:</strong> {{ center.address || 'Не указан' }}</p>
            <p><strong>📞 Телефон:</strong> {{ center.phone || 'Не указан' }}</p>
            <p><strong>✉️ Email:</strong> {{ center.email || 'Не указан' }}</p>
            <p><strong>⏰ Часы работы:</strong> {{ center.working_hours || 'Не указаны' }}</p>
          </div>
          
          <div class="center-actions">
            <button @click="viewCenter(center.id)" class="btn btn-primary">
              Подробнее
            </button>
            <button @click="viewRooms(center.id)" class="btn btn-secondary">
              Просмотреть залы
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Center Details Modal -->
    <div v-if="showCenterModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ selectedCenter?.name }}</h3>
          <button @click="closeModal" class="btn btn-sm btn-danger">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="center-details">
            <p><strong>Адрес:</strong> {{ selectedCenter?.address || 'Не указан' }}</p>
            <p><strong>Телефон:</strong> {{ selectedCenter?.phone || 'Не указан' }}</p>
            <p><strong>Email:</strong> {{ selectedCenter?.email || 'Не указан' }}</p>
            <p><strong>Часы работы:</strong> {{ selectedCenter?.working_hours || 'Не указаны' }}</p>
          </div>
          
          <div v-if="centerRooms.length > 0" class="rooms-section">
            <h4>Залы</h4>
            <div class="rooms-list">
              <div v-for="room in centerRooms" :key="room.id" class="room-item">
                <h5>{{ room.name }}</h5>
                <p>{{ room.description || 'Нет описания' }}</p>
                <p><small>Вместимость: {{ room.capacity || 'Не указана' }}</small></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { fitnessAPI } from '../../services/api'

export default {
  name: 'FitnessCenters',
  setup() {
    const centers = ref([])
    const centerRooms = ref([])
    const isLoading = ref(false)
    const showCenterModal = ref(false)
    const selectedCenter = ref(null)
    
    const fetchCenters = async () => {
      isLoading.value = true
      try {
        const response = await fitnessAPI.getCenters()
        centers.value = response.data
      } catch (error) {
        console.error('Error fetching centers:', error)
      } finally {
        isLoading.value = false
      }
    }
    
    const viewCenter = async (centerId) => {
      try {
        const [centerRes, roomsRes] = await Promise.all([
          fitnessAPI.getCenter(centerId),
          fitnessAPI.getRooms({ fitness_center_id: centerId })
        ])
        
        selectedCenter.value = centerRes.data
        centerRooms.value = roomsRes.data
        showCenterModal.value = true
      } catch (error) {
        console.error('Error fetching center details:', error)
      }
    }
    
    const viewRooms = async (centerId) => {
      // Можно реализовать отдельную страницу с залами
      console.log('View rooms for center:', centerId)
    }
    
    const closeModal = () => {
      showCenterModal.value = false
      selectedCenter.value = null
      centerRooms.value = []
    }
    
    onMounted(() => {
      fetchCenters()
    })
    
    return {
      centers,
      centerRooms,
      isLoading,
      showCenterModal,
      selectedCenter,
      fetchCenters,
      viewCenter,
      viewRooms,
      closeModal
    }
  }
}
</script>

<style scoped>
.centers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 30px;
  margin-top: 30px;
}

.center-card {
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
}

.center-card:hover {
  transform: translateY(-5px);
}

.center-image {
  height: 200px;
  background: linear-gradient(135deg, var(--accent-orange), var(--accent-purple));
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius) var(--radius) 0 0;
}

.image-placeholder {
  font-size: 4rem;
}

.center-content {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.center-title {
  color: var(--accent-orange);
  margin-bottom: 15px;
}

.center-info {
  flex: 1;
  margin-bottom: 20px;
}

.center-info p {
  margin: 5px 0;
  color: var(--text-muted);
}

.center-info strong {
  color: var(--text-light);
}

.center-actions {
  display: flex;
  gap: 10px;
  margin-top: auto;
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

.center-details p {
  margin: 10px 0;
}

.rooms-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.rooms-list {
  margin-top: 10px;
}

.room-item {
  padding: 10px;
  background-color: var(--primary-dark);
  border-radius: var(--radius);
  margin-bottom: 10px;
}

.room-item h5 {
  color: var(--accent-orange);
  margin-bottom: 5px;
}
</style>