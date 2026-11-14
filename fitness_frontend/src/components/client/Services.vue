<template>
  <div class="container">
    <h1 class="page-title">Услуги</h1>
    
    <div v-if="isLoading" class="loader"></div>
    
    <div v-else class="services-grid">
      <div v-for="service in services" :key="service.id" class="card service-card">
        <div class="service-header">
          <h3 class="service-title">{{ service.name }}</h3>
          <span v-if="service.price" class="service-price">
            {{ service.price }} ₽
          </span>
        </div>
        
        <div class="service-body">
          <p class="service-description">
            {{ service.description || 'Описание отсутствует' }}
          </p>
          
          <div v-if="service.duration" class="service-meta">
            <span class="duration">⏱ {{ service.duration }} мин</span>
          </div>
        </div>
        
        <div class="service-actions">
          <button @click="viewServiceSchedule(service.id)" class="btn btn-primary">
            Посмотреть расписание
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { fitnessAPI } from '../../services/api'

export default {
  name: 'Services',
  setup() {
    const router = useRouter()
    
    const services = ref([])
    const isLoading = ref(false)
    
    const fetchServices = async () => {
      isLoading.value = true
      try {
        const response = await fitnessAPI.getServices()
        services.value = response.data
      } catch (error) {
        console.error('Error fetching services:', error)
      } finally {
        isLoading.value = false
      }
    }
    
    const viewServiceSchedule = (serviceId) => {
      router.push({
        path: '/schedule',
        query: { serviceId }
      })
    }
    
    onMounted(() => {
      fetchServices()
    })
    
    return {
      services,
      isLoading,
      fetchServices,
      viewServiceSchedule
    }
  }
}
</script>

<style scoped>
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 30px;
}

.service-card {
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
}

.service-card:hover {
  transform: translateY(-5px);
}

.service-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
}

.service-title {
  color: var(--accent-orange);
  margin: 0;
}

.service-price {
  background: linear-gradient(135deg, var(--accent-orange), var(--accent-purple));
  color: white;
  padding: 5px 10px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.service-body {
  flex: 1;
  margin-bottom: 20px;
}

.service-description {
  color: var(--text-muted);
  line-height: 1.6;
}

.service-meta {
  margin-top: 15px;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.service-actions {
  margin-top: auto;
}
</style>