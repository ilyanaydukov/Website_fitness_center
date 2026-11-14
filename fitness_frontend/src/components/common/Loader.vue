<template>
  <div class="loader-container">
    <div class="loader"></div>
    <p v-if="message" class="loader-message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'Loader',
  props: {
    message: {
      type: String,
      default: 'Загрузка...'
    }
  }
}
</script>

<style scoped>
.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.loader {
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--accent-orange);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

.loader-message {
  margin-top: 15px;
  color: var(--text-muted);
  text-align: center;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>