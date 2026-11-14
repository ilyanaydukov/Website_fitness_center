<template>
  <div class="about">
    <div class="container">
      <h1 class="page-title">О нас</h1>
      
      <div class="about-content">
        <section class="about-section card">
          <h2>Наша миссия</h2>
          <p>
            Мы стремимся сделать фитнес доступным и приятным для каждого. 
            Наша цель — помочь людям улучшить качество жизни через регулярные 
            физические нагрузки и здоровый образ жизни.
          </p>
        </section>
        
        <section class="about-section card">
          <h2>Наши преимущества</h2>
          <div class="advantages-grid">
            <div class="advantage">
              <div class="advantage-icon">🏋️‍♂️</div>
              <h3>Современное оборудование</h3>
              <p>Только новейшие тренажеры от мировых производителей</p>
            </div>
            <div class="advantage">
              <div class="advantage-icon">👨‍🏫</div>
              <h3>Профессиональные тренеры</h3>
              <p>Сертифицированные специалисты с многолетним опытом</p>
            </div>
            <div class="advantage">
              <div class="advantage-icon">💻</div>
              <h3>Цифровая система</h3>
              <p>Удобное онлайн-расписание и запись на занятия</p>
            </div>
            <div class="advantage">
              <div class="advantage-icon">👨‍👩‍👧‍👦</div>
              <h3>Для всей семьи</h3>
              <p>Программы для детей, взрослых и пожилых людей</p>
            </div>
          </div>
        </section>
        
        <section class="about-section card">
          <h2>Наши ценности</h2>
          <ul class="values-list">
            <li>🚀 <strong>Инновации:</strong> Постоянное развитие и внедрение новых технологий</li>
            <li>❤️ <strong>Забота:</strong> Индивидуальный подход к каждому клиенту</li>
            <li>🤝 <strong>Сообщество:</strong> Создание дружеской атмосферы и поддержка</li>
            <li>🏆 <strong>Результаты:</strong> Помощь в достижении ваших спортивных целей</li>
            <li>🌱 <strong>Здоровье:</strong> Пропаганда здорового образа жизни</li>
          </ul>
        </section>
        
        <section class="about-section card">
          <h2>Контакты</h2>
          <div class="contact-info">
            <div class="contact-item">
              <strong>📞 Телефон:</strong> +7 (XXX) XXX-XX-XX
            </div>
            <div class="contact-item">
              <strong>✉️ Email:</strong> info@fitness-center.ru
            </div>
            <div class="contact-item">
              <strong>📍 Адрес:</strong> г. Томск, ул. Примерная, 123
            </div>
            <div class="contact-item">
              <strong>⏰ Часы работы:</strong> Пн-Вс: 6:00 - 23:00
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.about-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.about-section {
  padding: 30px;
}

.about-section h2 {
  color: var(--accent-orange);
  margin-bottom: 20px;
  font-size: 1.8rem;
}

.about-section p {
  color: var(--text-muted);
  line-height: 1.6;
  font-size: 1.1rem;
}

.advantages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-top: 20px;
}

.advantage {
  text-align: center;
  padding: 20px;
}

.advantage-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.advantage h3 {
  color: var(--accent-orange);
  margin-bottom: 10px;
  font-size: 1.3rem;
}

.advantage p {
  color: var(--text-muted);
  font-size: 1rem;
  line-height: 1.5;
}

.values-list {
  list-style: none;
  padding: 0;
}

.values-list li {
  margin-bottom: 15px;
  padding: 15px;
  background-color: var(--primary-dark);
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  gap: 15px;
}

.values-list strong {
  color: var(--accent-orange);
  margin-right: 10px;
}

.contact-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.contact-item {
  padding: 15px;
  background-color: var(--primary-dark);
  border-radius: var(--radius);
  color: var(--text-muted);
}

.contact-item strong {
  color: var(--text-light);
  margin-right: 10px;
}

@media (max-width: 768px) {
  .advantages-grid {
    grid-template-columns: 1fr;
  }
  
  .contact-info {
    grid-template-columns: 1fr;
  }
  
  .values-list li {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }
}
</style>