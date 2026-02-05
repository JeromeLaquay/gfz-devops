<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <PageHeader title="Messages de contact" />
    
    <div class="mt-6">
      <div v-if="loading" class="text-center py-8">
        <p class="text-gray-500">Chargement des messages...</p>
      </div>
      
      <div v-else-if="messages.length === 0" class="text-center py-8">
        <p class="text-gray-500">Aucun message pour le moment</p>
      </div>
      
      <div v-else class="space-y-4">
        <div
          v-for="msg in messages"
          :key="msg.id"
          class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
        >
          <div class="flex justify-between items-start mb-2">
            <div>
              <h3 class="font-semibold text-dark">{{ msg.nom }}</h3>
              <p class="text-sm text-gray-600">{{ msg.email }}</p>
            </div>
            <span class="text-xs text-gray-500">{{ formatDate(msg.dateCreation) }}</span>
          </div>
          
          <div v-if="msg.sujet" class="mb-2">
            <span class="text-sm font-medium text-gray-700">Sujet: </span>
            <span class="text-sm text-gray-600">{{ msg.sujet }}</span>
          </div>
          
          <p class="text-gray-700 whitespace-pre-wrap">{{ msg.message }}</p>
          
          <div v-if="replyingTo === msg.id" class="mt-4 border-t border-gray-200 pt-4">
            <textarea
              v-model="replyMessage"
              placeholder="Tapez votre réponse..."
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
              rows="4"
            ></textarea>
            <div class="flex gap-2 mt-2">
              <button
                @click="sendReply(msg.id)"
                :disabled="!replyMessage.trim() || sendingReply"
                class="px-4 py-2 bg-secondary text-white rounded-lg hover:bg-secondary/90 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ sendingReply ? 'Envoi...' : 'Envoyer la réponse' }}
              </button>
              <button
                @click="cancelReply"
                class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
              >
                Annuler
              </button>
            </div>
          </div>
          
          <div v-else class="flex gap-3 mt-3">
            <button
              @click="startReply(msg.id)"
              class="text-sm text-secondary hover:text-secondary/80 transition font-semibold"
            >
              Répondre
            </button>
            <button
              @click="deleteMessage(msg.id)"
              class="text-sm text-red-600 hover:text-red-800 transition"
            >
              Supprimer
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'admin'
})

import { ref, onMounted } from 'vue'
import PageHeader from '~/components/PageHeader.vue'
import { useApi } from '~/composables/useApi'

const { apiFetch } = useApi()
const messages = ref([])
const loading = ref(true)
const replyingTo = ref(null)
const replyMessage = ref('')
const sendingReply = ref(false)

const loadMessages = async () => {
  loading.value = true
  try {
    const data = await apiFetch('/contact')
    messages.value = data
  } catch (err) {
    console.error('Erreur lors du chargement des messages:', err)
  } finally {
    loading.value = false
  }
}

const deleteMessage = async (id) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer ce message ?')) {
    return
  }
  
  try {
    await apiFetch(`/contact/${id}`, {
      method: 'DELETE'
    })
    messages.value = messages.value.filter(msg => msg.id !== id)
  } catch (err) {
    console.error('Erreur lors de la suppression:', err)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const startReply = (id) => {
  replyingTo.value = id
  replyMessage.value = ''
}

const cancelReply = () => {
  replyingTo.value = null
  replyMessage.value = ''
}

const sendReply = async (id) => {
  if (!replyMessage.value.trim()) return
  
  sendingReply.value = true
  try {
    await apiFetch(`/contact/${id}/reply`, {
      method: 'POST',
      body: {
        message: replyMessage.value
      }
    })
    alert('Réponse envoyée avec succès !')
    cancelReply()
  } catch (err) {
    console.error('Erreur lors de l\'envoi de la réponse:', err)
    alert('Erreur lors de l\'envoi de la réponse. Veuillez réessayer.')
  } finally {
    sendingReply.value = false
  }
}

onMounted(() => {
  loadMessages()
})
</script>
