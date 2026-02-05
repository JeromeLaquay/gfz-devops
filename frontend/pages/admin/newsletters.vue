<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <PageHeader title="Gestion des newsletters" />
    
    <div class="mt-6 space-y-6">
      <div>
        <h2 class="text-xl font-semibold text-dark mb-4">Envoyer une newsletter</h2>
        <form @submit.prevent="sendNewsletter" class="space-y-4">
          <div>
            <label for="sujet" class="block text-sm font-medium text-gray-700 mb-1">
              Sujet <span class="text-red-500">*</span>
            </label>
            <input
              id="sujet"
              v-model="newsletterForm.sujet"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
              placeholder="Sujet de la newsletter"
            />
          </div>
          
          <div>
            <label for="message" class="block text-sm font-medium text-gray-700 mb-1">
              Message <span class="text-red-500">*</span>
            </label>
            <textarea
              id="message"
              v-model="newsletterForm.message"
              required
              rows="8"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent resize-none"
              placeholder="Contenu de la newsletter..."
            ></textarea>
          </div>
          
          <button
            type="submit"
            :disabled="isSending"
            class="bg-secondary hover:bg-secondary-dark text-white font-semibold py-2 px-6 rounded-lg transition-colors disabled:opacity-50"
          >
            {{ isSending ? 'Envoi en cours...' : 'Envoyer la newsletter' }}
          </button>
          
          <div v-if="message" :class="messageType === 'success' ? 'text-green-600' : 'text-red-600'" class="text-sm">
            {{ message }}
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'admin'
})

import { ref } from 'vue'
import PageHeader from '~/components/PageHeader.vue'
import { useApi } from '~/composables/useApi'

const { apiFetch } = useApi()
const newsletterForm = ref({
  sujet: '',
  message: ''
})
const isSending = ref(false)
const message = ref('')
const messageType = ref('')

const sendNewsletter = async () => {
  if (!newsletterForm.value.sujet.trim() || !newsletterForm.value.message.trim()) {
    message.value = 'Veuillez remplir tous les champs'
    messageType.value = 'error'
    return
  }

  isSending.value = true
  message.value = ''
  
  try {
    await apiFetch('/newsletter/send', {
      method: 'POST',
      body: {
        sujet: newsletterForm.value.sujet,
        message: newsletterForm.value.message
      }
    })
    message.value = 'Newsletter envoyée avec succès à tous les abonnés'
    messageType.value = 'success'
    newsletterForm.value = { sujet: '', message: '' }
  } catch (err) {
    console.error('Erreur lors de l\'envoi de la newsletter:', err)
    message.value = 'Erreur lors de l\'envoi de la newsletter. Veuillez réessayer.'
    messageType.value = 'error'
  } finally {
    isSending.value = false
  }
}
</script>
