<template>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-brand">
        <router-link to="/" class="logo">
          <span class="logo-text">FITNESS</span>
          <span class="logo-accent">CENTER</span>
        </router-link>
      </div>
      
      <div class="navbar-menu">
        <div class="nav-links">
          <router-link to="/schedule" class="nav-link">
            📅 Расписание
          </router-link>
          <router-link to="/services" class="nav-link">
            💪 Услуги
          </router-link>
          <router-link to="/trainers" class="nav-link">
            👨‍🏫 Тренеры
          </router-link>
          <router-link to="/centers" class="nav-link">
            🏋️ Залы
          </router-link>
          <router-link to="/subscriptions" class="nav-link">
            💰 Абонементы
          </router-link>
        </div>
        
        <!-- Для отладки показываем состояние -->
        <div class="debug-info" v-if="showDebug">
          <small>
            Auth: {{ isAuthenticated ? 'YES' : 'NO' }}
            User: {{ user?.email || 'none' }}
          </small>
        </div>
        
        <div v-if="!isAuthenticated" class="auth-links">
          <router-link to="/login" class="nav-link">
            Вход
          </router-link>
          <router-link to="/register" class="btn btn-sm btn-primary">
            Регистрация
          </router-link>
        </div>
        
        <div v-else class="user-menu">
          <router-link v-if="isEmployee" to="/admin" class="nav-link">
            🛠 Админ панель
          </router-link>
          
          <div class="user-dropdown">
            <button class="user-toggle">
              👤 {{ fullName || 'Профиль' }}
            </button>
            <div class="dropdown-menu">
              <router-link to="/profile" class="dropdown-item">
                Мой профиль
              </router-link>
              <router-link to="/dashboard" class="dropdown-item">
                Личный кабинет
              </router-link>
              <div class="dropdown-divider"></div>
              <button @click="logout" class="dropdown-item logout">
                Выйти
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'

export default {
  name: 'Navbar',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const logout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    return {
      isAuthenticated: computed(() => authStore.isAuthenticated),
      isEmployee: computed(() => authStore.isEmployee),
      user: computed(() => authStore.user),
      fullName: computed(() => authStore.fullName),
      showDebug: computed(() => process.env.NODE_ENV === 'development'),
      logout
    }
  }
}
</script>

<style scoped>
.navbar {
  background: linear-gradient(135deg, var(--primary-dark) 0%, #2a2a2a 100%);
  border-bottom: 1px solid var(--border-color);
  padding: 15px 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand .logo {
  font-size: 1.8rem;
  font-weight: 700;
  text-decoration: none;
}

.logo-text {
  color: var(--text-light);
}

.logo-accent {
  color: var(--accent-orange);
  margin-left: 5px;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-links {
  display: flex;
  gap: 15px;
}

.auth-links {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-dropdown {
  position: relative;
}

.user-toggle {
  background: none;
  border: 1px solid var(--accent-orange);
  color: var(--accent-orange);
  padding: 8px 15px;
  border-radius: var(--radius);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: var(--transition);
}

.user-toggle:hover {
  background-color: rgba(255, 107, 53, 0.1);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: var(--secondary-dark);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  min-width: 200px;
  margin-top: 10px;
  display: none;
  flex-direction: column;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  z-index: 1000;
}

.user-dropdown:hover .dropdown-menu {
  display: flex;
}

.dropdown-item {
  padding: 12px 15px;
  color: var(--text-light);
  text-decoration: none;
  transition: var(--transition);
  text-align: left;
  background: none;
  border: none;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: var(--primary-dark);
  color: var(--accent-orange);
}

.dropdown-divider {
  height: 1px;
  background-color: var(--border-color);
  margin: 5px 0;
}

.dropdown-item.logout {
  color: var(--danger);
}

.nav-link {
  color: var(--text-light);
  text-decoration: none;
  padding: 8px 12px;
  border-radius: var(--radius);
  transition: var(--transition);
  font-weight: 500;
}

.nav-link:hover {
  color: var(--accent-orange);
  background-color: rgba(255, 107, 53, 0.1);
}

.nav-link.router-link-active {
  color: var(--accent-orange);
  background-color: rgba(255, 107, 53, 0.1);
}

@media (max-width: 768px) {
  .navbar .container {
    flex-direction: column;
    gap: 15px;
  }
  
  .navbar-menu {
    width: 100%;
    justify-content: space-between;
  }
  
  .nav-links {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    width: 100%;
  }
  
  .nav-link {
    text-align: center;
    font-size: 0.9rem;
    padding: 8px 5px;
  }
}
</style>