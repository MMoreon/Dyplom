<template>
  <div class="register-container">
    <div class="register-card">
      <h2 class="register-title">Регистрация</h2>
      
      <form @submit.prevent="submitForm" class="register-form">
        <div class="form-group">
          <label for="username" class="form-label">Логин</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            class="form-input"
            placeholder="Введите логин"
            required
          >
        </div>

        <div class="form-group">
          <label for="email" class="form-label">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="form-input"
            placeholder="Введите email"
            required
          >
        </div>

        <div class="form-group">
          <label for="password" class="form-label">Пароль</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="form-input"
            placeholder="Введите пароль (минимум 8 символов)"
            required
          >
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>

        <div class="login-link">
          Уже есть аккаунт? <router-link to="/login">Войдите</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  setup() {
    const router = useRouter()
    const form = ref({
      username: '',
      email: '',
      password: ''
    })
    const errorMessage = ref('')
    const loading = ref(false)

    const submitForm = async () => {
      try {
        loading.value = true
        errorMessage.value = ''
        
        await axios.post('http://localhost:8000/users/', form.value)
        
        router.push('/login')
      } catch (error) {
        errorMessage.value = error.response?.data?.detail || 'Ошибка регистрации'
        console.error('Registration error:', error)
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      errorMessage,
      loading,
      submitForm
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
  background-color: #f5f5f5;
}

.register-card {
  width: 100%;
  max-width: 100%;
  padding: 3rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.register-title {
  text-align: center;
  color: #1E5945;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.error-message {
  color: #dc3545;
  margin-bottom: 1rem;
  text-align: center;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
  color: #666;
}

.login-link a {
  color: #3F888F;
  text-decoration: none;
  font-weight: 500;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>