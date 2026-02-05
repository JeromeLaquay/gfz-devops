<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <PageHeader title="Gestion des administrateurs" />
    
    <div class="mt-6 space-y-6">
      <div>
        <h2 class="text-xl font-semibold text-dark mb-4">Ajouter un administrateur</h2>
        <form @submit.prevent="addUser" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="username" class="block text-sm font-medium text-gray-700 mb-1">
                Nom d'utilisateur <span class="text-red-500">*</span>
              </label>
              <input
                id="username"
                v-model="userForm.username"
                type="text"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
                placeholder="username"
              />
            </div>
            
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                id="email"
                v-model="userForm.email"
                type="email"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
                placeholder="email@example.com"
              />
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700 mb-1">
                Nom complet
              </label>
              <input
                id="name"
                v-model="userForm.name"
                type="text"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
                placeholder="Nom complet"
              />
            </div>
          </div>
          
          <button
            type="submit"
            :disabled="isSubmitting"
            class="bg-secondary hover:bg-secondary-dark text-white font-semibold py-2 px-6 rounded-lg transition-colors disabled:opacity-50"
          >
            {{ isSubmitting ? 'Ajout...' : 'Ajouter l\'administrateur' }}
          </button>
          
          <div v-if="message" :class="messageType === 'success' ? 'text-green-600' : 'text-red-600'" class="text-sm">
            {{ message }}
          </div>
        </form>
      </div>
      
      <div>
        <h2 class="text-xl font-semibold text-dark mb-4">Liste des administrateurs</h2>
        <div v-if="loading" class="text-center py-8">
          <p class="text-gray-500">Chargement...</p>
        </div>
        <div v-else-if="users.length === 0" class="text-center py-8">
          <p class="text-gray-500">Aucun administrateur</p>
        </div>
        <div v-else class="space-y-2">
          <div
            v-for="user in users"
            :key="user.id"
            class="flex justify-between items-center p-3 border border-gray-200 rounded-lg"
          >
            <div>
              <p class="font-semibold">{{ user.name || user.username }}</p>
              <p class="text-sm text-gray-600">{{ user.email || user.username }}</p>
            </div>
            <button
              @click="deleteUser(user.id)"
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
const userForm = ref({
  username: '',
  email: '',
  name: ''
})
const users = ref([])
const isSubmitting = ref(false)
const loading = ref(true)
const message = ref('')
const messageType = ref('')

const loadUsers = async () => {
  loading.value = true
  try {
    const data = await apiFetch('/users')
    users.value = data
  } catch (err) {
    console.error('Erreur lors du chargement des utilisateurs:', err)
  } finally {
    loading.value = false
  }
}

const addUser = async () => {
  isSubmitting.value = true
  message.value = ''
  
  try {
    await apiFetch('/users', {
      method: 'POST',
      body: userForm.value
    })
    
    message.value = 'Administrateur ajouté avec succès. Un email a été envoyé pour créer le mot de passe.'
    messageType.value = 'success'
    userForm.value = { username: '', email: '', name: '' }
    await loadUsers()
  } catch (err) {
    message.value = err?.data?.message || 'Erreur lors de l\'ajout'
    messageType.value = 'error'
  } finally {
    isSubmitting.value = false
  }
}

const deleteUser = async (id) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer cet administrateur ?')) {
    return
  }
  
  try {
    await apiFetch(`/users/${id}`, {
      method: 'DELETE'
    })
    users.value = users.value.filter(user => user.id !== id)
  } catch (err) {
    console.error('Erreur lors de la suppression:', err)
  }
}

onMounted(() => {
  loadUsers()
})
</script>
