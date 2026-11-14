<template>
  <div class="not-found">
    <div class="container">
      <div class="error-content">
        <div class="error-code">404</div>
        <h1 class="error-title">Страница не найдена</h1>
        <p class="error-message">
          Запрашиваемая страница не существует или была перемещена.
        </p>
        <div class="error-actions">
          <router-link to="/" class="btn btn-primary btn-lg">
            Вернуться на главную
          </router-link>
          <button @click="$router.back()" class="btn btn-secondary btn-lg">
            Вернуться назад
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>

<style scoped>
.not-found {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.error-content {
  max-width: 600px;
  margin: 0 auto;
  padding: 40px;
}

.error-code {
  font-size: 8rem;
  font-weight: 900;
  background: linear-gradient(to right, var(--accent-orange), var(--accent-purple));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  line-height: 1;
  margin-bottom: 20px;
}

.error-title {
  font-size: 2.5rem;
  color: var(--text-light);
  margin-bottom: 20px;
}

.error-message {
  font-size: 1.2rem;
  color: var(--text-muted);
  margin-bottom: 40px;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
}

@media (max-width: 768px) {
  .error-code {
    font-size: 6rem;
  }
  
  .error-title {
    font-size: 2rem;
  }
  
  .error-actions {
    flex-direction: column;
  }
}
</style>