<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <PageHeader title="Ajouter une offre d'emploi" />
    
    <form @submit.prevent="submitForm" class="space-y-4 mt-6">
      <div>
        <label for="titre" class="block text-sm font-medium text-gray-700 mb-1">
          Titre <span class="text-red-500">*</span>
        </label>
        <input
          id="titre"
          v-model="form.titre"
          type="text"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
          placeholder="Titre de l'offre"
        />
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="type" class="block text-sm font-medium text-gray-700 mb-1">
            Type
          </label>
          <input
            id="type"
            v-model="form.type"
            type="text"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
            placeholder="CDI, CDD, Stage..."
          />
        </div>
        
        <div>
          <label for="localisation" class="block text-sm font-medium text-gray-700 mb-1">
            Localisation
          </label>
          <input
            id="localisation"
            v-model="form.localisation"
            type="text"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
            placeholder="Ville, Pays..."
          />
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="duree" class="block text-sm font-medium text-gray-700 mb-1">
            Durée
          </label>
          <input
            id="duree"
            v-model="form.duree"
            type="text"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
            placeholder="6 mois, 1 an..."
          />
        </div>
        
        <div>
          <label for="dateExpiration" class="block text-sm font-medium text-gray-700 mb-1">
            Date d'expiration
          </label>
          <input
            id="dateExpiration"
            v-model="form.dateExpiration"
            type="date"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
          />
        </div>
      </div>
      
      <div>
        <label for="resume" class="block text-sm font-medium text-gray-700 mb-1">
          Résumé
        </label>
        <textarea
          id="resume"
          v-model="form.resume"
          rows="6"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent resize-none"
          placeholder="Description de l'offre..."
        ></textarea>
      </div>
      
      <button
        type="submit"
        :disabled="isSubmitting"
        class="bg-secondary hover:bg-secondary-dark text-white font-semibold py-2 px-6 rounded-lg transition-colors disabled:opacity-50"
      >
        {{ isSubmitting ? 'Enregistrement...' : 'Enregistrer l\'offre' }}
      </button>
      
      <div v-if="message" :class="messageType === 'success' ? 'text-green-600' : 'text-red-600'" class="text-sm">
        {{ message }}
      </div>
    </form>
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
const form = ref({
  titre: '',
  type: '',
  localisation: '',
  duree: '',
  dateExpiration: '',
  resume: ''
})
const isSubmitting = ref(false)
const message = ref('')
const messageType = ref('')

const submitForm = async () => {
  isSubmitting.value = true
  message.value = ''
  
  try {
    await apiFetch('/offres-emploi', {
      method: 'POST',
      body: form.value
    })
    
    message.value = 'Offre d\'emploi enregistrée avec succès'
    messageType.value = 'success'
    form.value = { titre: '', type: '', localisation: '', duree: '', dateExpiration: '', resume: '' }
  } catch (err) {
    message.value = err?.data?.message || 'Erreur lors de l\'enregistrement'
    messageType.value = 'error'
  } finally {
    isSubmitting.value = false
  }
}
</script>
