<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h4 class="footer-title">Фитнес-центр</h4>
          <p>Современное фитнес-пространство для вашего здоровья и красоты</p>
        </div>
        
        <div class="footer-section">
          <h4 class="footer-title">Навигация</h4>
          <ul class="footer-links">
            <li><router-link to="/">Главная</router-link></li>
            <li><router-link to="/centers">Фитнес-центры</router-link></li>
            <li><router-link to="/services">Услуги</router-link></li>
            <li><router-link to="/schedule">Расписание</router-link></li>
            <li><router-link to="/about">О нас</router-link></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h4 class="footer-title">Контакты</h4>
          <ul class="footer-contacts">
            <li>📞 +7 (XXX) XXX-XX-XX</li>
            <li>✉️ info@fitness-center.ru</li>
            <li>📍 г. Томск, ул. Примерная, 123</li>
          </ul>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; {{ currentYear }} Фитнес-центр. Все права защищены.</p>
      </div>
    </div>
  </footer>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'Footer',
  setup() {
    const currentYear = computed(() => new Date().getFullYear())
    
    return {
      currentYear
    }
  }
}
</script>

<style scoped>
.footer {
  background-color: var(--primary-dark);
  border-top: 1px solid var(--border-color);
  padding: 40px 0 20px;
  margin-top: auto;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  margin-bottom: 40px;
}

.footer-section {
  margin-bottom: 20px;
}

.footer-title {
  color: var(--accent-orange);
  margin-bottom: 15px;
  font-size: 1.2rem;
}

.footer-links {
  list-style: none;
  padding: 0;
}

.footer-links li {
  margin-bottom: 10px;
}

.footer-links a {
  color: var(--text-muted);
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: var(--accent-orange);
}

.footer-contacts {
  list-style: none;
  padding: 0;
  color: var(--text-muted);
}

.footer-contacts li {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
  color: var(--text-muted);
  font-size: 0.9rem;
}
</style>