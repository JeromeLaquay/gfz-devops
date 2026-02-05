<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <PageHeader title="Contact" />
    <!-- Informations de contact -->
    <div>
          <h2 class="text-xl font-semibold text-dark mb-4">Informations de contact</h2>
          <div class="space-y-6">
            <div>
              <h3 class="font-semibold text-dark mb-2">Association GFZ</h3>
              <p class="text-gray-700 mb-2">
                <strong>Fonction:</strong> Groupe Français des Zéolithes
              </p>
              <p class="text-gray-700">
                <strong>Adresse:</strong><br />
                URA 1106 du CNRS<br />
                Université Pierre et Marie Curie<br />
                4 place Jussieu<br />
                PARIS cedex 05<br />
                75252<br />
                France
              </p>
              <p class="text-gray-700 mt-2">
                <a href="http://gfz-online.fr" target="_blank" class="text-blue-600 hover:underline">
                  http://gfz-online.fr
                </a>
              </p>
            </div>
          </div>
        </div>
        
    <div class="mt-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Formulaire de contact -->
        <div>
          <h2 class="text-xl font-semibold text-dark mb-4">Envoyez-nous un message</h2>
          <form @submit.prevent="submitForm" class="space-y-4">
            <div>
              <label for="nom" class="block text-sm font-medium text-gray-700 mb-1">
                Nom <span class="text-red-500">*</span>
              </label>
              <input
                id="nom"
                v-model="form.nom"
                type="text"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
                placeholder="Votre nom"
              />
            </div>
            
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
                Email <span class="text-red-500">*</span>
              </label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
                placeholder="votre.email@example.com"
              />
            </div>
            
            <div>
              <label for="sujet" class="block text-sm font-medium text-gray-700 mb-1">
                Sujet <span class="text-red-500">*</span>
              </label>
              <input
                id="sujet"
                v-model="form.sujet"
                type="text"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
                placeholder="Objet de votre message"
              />
            </div>
            
            <div>
              <label for="message" class="block text-sm font-medium text-gray-700 mb-1">
                Message <span class="text-red-500">*</span>
              </label>
              <textarea
                id="message"
                v-model="form.message"
                required
                rows="6"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent resize-none"
                placeholder="Votre message..."
              ></textarea>
            </div>
            
            <div>
              <label class="flex items-center">
                <input
                  v-model="form.sendCopy"
                  type="checkbox"
                  class="mr-2 h-4 w-4 text-secondary focus:ring-secondary border-gray-300 rounded"
                />
                <span class="text-sm text-gray-700">
                  Envoyer une copie à votre adresse (facultatif)
                </span>
              </label>
            </div>
            
            <div>
              <label for="captcha" class="block text-sm font-medium text-gray-700 mb-1">
                Captcha <span class="text-red-500">*</span>
              </label>
              <div class="flex items-center gap-4">
                <div class="flex-1">
                  <input
                    id="captcha"
                    v-model="form.captcha"
                    type="text"
                    required
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
                    placeholder="Entrez le code captcha"
                  />
                </div>
                <div class="bg-gray-100 border-2 border-gray-300 px-4 py-2 rounded-lg font-mono text-lg font-bold text-gray-700 select-none">
                  {{ captchaCode }}
                </div>
                <button
                  type="button"
                  @click="generateCaptcha"
                  class="text-sm text-secondary hover:underline"
                  title="Rafraîchir le captcha"
                >
                  🔄
                </button>
              </div>
            </div>
            
            <button
              type="submit"
              :disabled="isSubmitting"
              class="w-full bg-secondary hover:bg-secondary-dark text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isSubmitting ? 'Envoi en cours...' : 'Envoyer le message' }}
            </button>
            
            <div v-if="message" :class="messageType === 'success' ? 'text-green-600' : 'text-red-600'" class="text-sm mt-2">
              {{ message }}
            </div>
          </form>
        </div>
        
        
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PageHeader from '~/components/PageHeader.vue'

const form = ref({
  nom: '',
  email: '',
  sujet: '',
  message: '',
  sendCopy: false,
  captcha: ''
})

const captchaCode = ref('')
const isSubmitting = ref(false)
const message = ref('')
const messageType = ref('')

const generateCaptcha = () => {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  captchaCode.value = Array.from({ length: 5 }, () => chars[Math.floor(Math.random() * chars.length)]).join('')
  form.value.captcha = ''
}

// Générer le captcha au chargement
onMounted(() => {
  generateCaptcha()
})

const submitForm = async () => {
  if (form.value.captcha.toUpperCase() !== captchaCode.value) {
    message.value = 'Le code captcha est incorrect. Veuillez réessayer.'
    messageType.value = 'error'
    generateCaptcha()
    return
  }
  
  isSubmitting.value = true
  message.value = ''
  
  try {
    const { apiFetch } = useApi()
    const payload = {
      nom: form.value.nom,
      email: form.value.email,
      sujet: form.value.sujet || '',
      message: form.value.message
    }
    
    await apiFetch('/contact', {
      method: 'POST',
      body: payload
    })
    
    message.value = 'Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.'
    messageType.value = 'success'
    
    form.value = {
      nom: '',
      email: '',
      sujet: '',
      message: '',
      sendCopy: false,
      captcha: ''
    }
    generateCaptcha()
  } catch (error) {
    const errorMessage = error?.data?.message || error?.message || 'Une erreur est survenue'
    message.value = `Erreur lors de l'envoi : ${errorMessage}. Veuillez réessayer.`
    messageType.value = 'error'
    generateCaptcha()
  } finally {
    isSubmitting.value = false
  }
}
</script>
