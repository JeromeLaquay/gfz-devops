<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <PageHeader title="Mot de passe oublié" />
    
    <div class="mt-6 max-w-md mx-auto">
      <p class="text-gray-700 mb-6">
        Entrez votre adresse email ou votre identifiant pour recevoir un lien 
        de réinitialisation de mot de passe.
      </p>
      
      <form @submit.prevent="handleForgotPassword" class="space-y-4">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
            Email ou identifiant <span class="text-red-500">*</span>
          </label>
          <input
            id="email"
            v-model="email"
            type="text"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
            placeholder="Votre email ou identifiant"
          />
        </div>
        
        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-secondary text-white py-2 px-4 rounded-lg hover:bg-secondary/90 transition disabled:opacity-50"
        >
          {{ loading ? 'Envoi...' : 'Envoyer le lien de réinitialisation' }}
        </button>
        
        <div v-if="message" :class="messageType === 'success' ? 'text-green-600' : 'text-red-600'" class="text-sm">
          {{ message }}
        </div>
      </form>
      
      <div class="mt-6 pt-6 border-t border-gray-200">
        <NuxtLink
          to="/"
          class="block text-center text-secondary hover:text-secondary/80 transition"
        >
          Retour à l'accueil
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PageHeader from '~/components/PageHeader.vue'
import { useApi } from '~/composables/useApi'

const { apiFetch } = useApi()
const email = ref('')
const loading = ref(false)
const message = ref('')
const messageType = ref('')

const handleForgotPassword = async () => {
  if (!email.value.trim()) {
    message.value = 'Veuillez entrer votre email ou identifiant'
    messageType.value = 'error'
    return
  }

  loading.value = true
  message.value = ''

  try {
    await apiFetch('/auth/forgot-password', {
      method: 'POST',
      body: {
        emailOrUsername: email.value
      }
    })
    
    message.value = 'Si un compte existe avec cet email/identifiant, un lien de réinitialisation a été envoyé.'
    messageType.value = 'success'
    email.value = ''
  } catch (err) {
    console.error('Erreur lors de la demande de réinitialisation:', err)
    message.value = 'Une erreur est survenue. Veuillez contacter l\'administrateur.'
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}
</script>
