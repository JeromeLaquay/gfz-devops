<template>
  <div class="bg-white rounded-lg shadow">
    <div class="bg-[#376299] px-4 py-2 border-b-2 border-secondary">
      <h3 class="text-white font-semibold uppercase">ESPACE BUREAU</h3>
    </div>
    <form @submit.prevent="handleLogin" class="p-4 space-y-3">
      <div class="flex items-center border border-gray-300 rounded">
        <span class="px-3 text-gray-500">👤</span>
        <input
          v-model="credentials.username"
          type="text"
          placeholder="Identifiant"
          required
          class="flex-1 py-2 pr-3 focus:outline-none focus:ring-2 focus:ring-secondary"
        />
      </div>
      <div class="flex items-center border border-gray-300 rounded">
        <span class="px-3 text-gray-500">🔒</span>
        <input
          v-model="credentials.password"
          type="password"
          placeholder="Mot de passe"
          required
          class="flex-1 py-2 pr-3 focus:outline-none focus:ring-2 focus:ring-secondary"
        />
      </div>
      <button
        type="submit"
        :disabled="loading"
        class="w-full bg-[#376299] text-white py-2 rounded hover:opacity-90 transition disabled:opacity-50"
      >
        {{ loading ? 'Connexion...' : 'Se connecter' }}
      </button>
      <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
      
      <div class="pt-2 border-t border-gray-200 space-y-2">
        <NuxtLink
          to="/forgot-username"
          class="block text-sm text-secondary hover:text-secondary/80 transition text-center"
        >
          Identifiant oublié ?
        </NuxtLink>
        <NuxtLink
          to="/forgot-password"
          class="block text-sm text-secondary hover:text-secondary/80 transition text-center"
        >
          Mot de passe oublié ?
        </NuxtLink>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
const credentials = ref({
  username: '',
  password: ''
})
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  
  try {
    await authStore.login(credentials.value)
    alert('Connexion réussie !')
    credentials.value = { username: '', password: '' }
  } catch (err) {
    const errorMessage = err?.data?.message || err?.message || 'Erreur de connexion'
    error.value = errorMessage
    console.error('Erreur de connexion:', err)
  } finally {
    loading.value = false
  }
}
</script>
