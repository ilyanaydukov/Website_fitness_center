import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fitnessAPI } from '../services/api'

export const useWorkoutsStore = defineStore('workouts', () => {
  const workouts = ref([])
  const isLoading = ref(false)
  const lastFetch = ref(null)
  const cacheDuration = 5 * 60 * 1000 // 5 минут

  const fetchWorkouts = async (params = {}) => {
    const now = Date.now()
    
    // Используем кэш, если данные не устарели
    if (lastFetch.value && (now - lastFetch.value < cacheDuration) && workouts.value.length > 0) {
      return workouts.value
    }
    
    isLoading.value = true
    try {
      const response = await fitnessAPI.getWorkouts(params)
      workouts.value = response.data
      lastFetch.value = now
      return workouts.value
    } catch (error) {
      console.error('Error fetching workouts:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const getWorkoutById = (id) => {
    return workouts.value.find(workout => workout.id === id)
  }

  const addWorkout = (workout) => {
    workouts.value.push(workout)
  }

  const updateWorkout = (id, updatedWorkout) => {
    const index = workouts.value.findIndex(workout => workout.id === id)
    if (index !== -1) {
      workouts.value[index] = { ...workouts.value[index], ...updatedWorkout }
    }
  }

  const deleteWorkout = (id) => {
    workouts.value = workouts.value.filter(workout => workout.id !== id)
  }

  const clearCache = () => {
    workouts.value = []
    lastFetch.value = null
  }

  return {
    workouts,
    isLoading,
    fetchWorkouts,
    getWorkoutById,
    addWorkout,
    updateWorkout,
    deleteWorkout,
    clearCache
  }
})