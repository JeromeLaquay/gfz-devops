<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="bg-white p-8 rounded-lg shadow">
        <h2 class="text-2xl font-bold text-center text-dark mb-6">
          Réinitialiser votre mot de passe
        </h2>
        
        <form @submit.prevent="resetPassword" class="space-y-4">
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
              Nouveau mot de passe <span class="text-red-500">*</span>
            </label>
            <input
              id="password"
              v-model="passwordForm.password"
              type="password"
              required
              minlength="6"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
              placeholder="Votre nouveau mot de passe"
            />
          </div>
          
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">
              Confirmer le mot de passe <span class="text-red-500">*</span>
            </label>
            <input
              id="confirmPassword"
              v-model="passwordForm.confirmPassword"
              type="password"
              required
              minlength="6"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
              placeholder="Confirmer votre nouveau mot de passe"
            />
          </div>
          
          <div v-if="message" :class="messageType === 'success' ? 'text-green-600' : 'text-red-600'" class="text-sm">
            {{ message }}
          </div>
          
          <button
            type="submit"
            :disabled="isSubmitting || !isFormValid"
            class="w-full bg-secondary hover:bg-secondary-dark text-white font-semibold py-2 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isSubmitting ? 'Réinitialisation...' : 'Réinitialiser le mot de passe' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApi } from '~/composables/useApi'

const route = useRoute()
const router = useRouter()
const { apiFetch } = useApi()

const passwordForm = ref({
  password: '',
  confirmPassword: ''
})
const isSubmitting = ref(false)
const message = ref('')
const messageType = ref('')
const token = ref('')

const isFormValid = computed(() => {
  return passwordForm.value.password.length >= 6 &&
         passwordForm.value.password === passwordForm.value.confirmPassword
})

onMounted(() => {
  token.value = route.query.token
  if (!token.value) {
    message.value = 'Token invalide ou manquant. Veuillez utiliser le lien reçu par email.'
    messageType.value = 'error'
  }
})

const resetPassword = async () => {
  if (passwordForm.value.password !== passwordForm.value.confirmPassword) {
    message.value = 'Les mots de passe ne correspondent pas'
    messageType.value = 'error'
    return
  }

  if (passwordForm.value.password.length < 6) {
    message.value = 'Le mot de passe doit contenir au moins 6 caractères'
    messageType.value = 'error'
    return
  }

  if (!token.value) {
    message.value = 'Token invalide. Veuillez utiliser le lien reçu par email.'
    messageType.value = 'error'
    return
  }

  isSubmitting.value = true
  message.value = ''

  try {
    await apiFetch('/users/set-password', {
      method: 'POST',
      body: {
        token: token.value,
        password: passwordForm.value.password
      }
    })

    message.value = 'Mot de passe réinitialisé avec succès ! Redirection vers la page de connexion...'
    messageType.value = 'success'
    
    setTimeout(() => {
      router.push('/')
    }, 2000)
  } catch (err) {
    console.error('Erreur lors de la réinitialisation:', err)
    message.value = err?.data?.message || 'Erreur lors de la réinitialisation. Le token est peut-être invalide ou expiré.'
    messageType.value = 'error'
  } finally {
    isSubmitting.value = false
  }
}
</script>
