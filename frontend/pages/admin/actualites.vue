<template>
  <ClientOnly>
    <div class="space-y-6">
      <div class="bg-white p-6 rounded-lg shadow">
        <PageHeader :title="selectedArticle ? 'Modifier une actualité' : 'Ajouter une actualité'" />
      
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
              placeholder="Titre de l'actualité"
            />
          </div>
          
          <div>
            <label for="dateCreation" class="block text-sm font-medium text-gray-700 mb-1">
              Date de création
            </label>
            <input
              id="dateCreation"
              v-model="form.dateCreation"
              type="datetime-local"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
            />
          </div>
          
          <div>
            <label for="image" class="block text-sm font-medium text-gray-700 mb-1">
              Image
            </label>
            <div class="space-y-2">
              <div class="flex gap-2">
                <input
                  id="imageFile"
                  type="file"
                  accept="image/*"
                  @change="handleImageUpload"
                  class="hidden"
                />
                <label
                  for="imageFile"
                  class="cursor-pointer bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-2 px-4 rounded-lg border border-gray-300 transition-colors"
                >
                  {{ imageFile ? 'Changer l\'image' : 'Choisir une image' }}
                </label>
                <input
                  v-if="form.image"
                  v-model="form.image"
                  type="text"
                  placeholder="Ou entrer une URL"
                  class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
                />
                <button
                  v-if="form.image"
                  type="button"
                  @click="form.image = ''; imageFile = null; imagePreview = ''"
                  class="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                >
                  Supprimer
                </button>
              </div>
              <div v-if="imagePreview" class="mt-2">
                <img
                  :src="imagePreview"
                  alt="Aperçu"
                  class="max-w-xs max-h-48 rounded-lg border border-gray-300"
                />
              </div>
              <p class="text-xs text-gray-500 mt-1">
                L'image sera stockée directement en base de données (format base64)
              </p>
            </div>
          </div>
          
          <div>
            <label for="contenu" class="block text-sm font-medium text-gray-700 mb-1">
              Contenu
            </label>
            <div class="mb-2">
              <button
                type="button"
                @click="showDocumentsModal = true"
                class="text-sm bg-blue-100 hover:bg-blue-200 text-blue-700 py-1 px-3 rounded transition-colors"
              >
                📎 Insérer un lien vers un document
              </button>
            </div>
            <RichTextEditor
              id="contenu"
              v-model="form.contenu"
            />
          </div>
          
          <div class="flex gap-4">
            <button
              type="submit"
              :disabled="isSubmitting"
              class="bg-secondary hover:bg-secondary-dark text-white font-semibold py-2 px-6 rounded-lg transition-colors disabled:opacity-50"
            >
              {{ isSubmitting ? 'Enregistrement...' : (selectedArticle ? 'Mettre à jour' : 'Enregistrer') }}
            </button>
            <button
              v-if="selectedArticle"
              type="button"
              @click="resetForm"
              class="bg-gray-500 hover:bg-gray-600 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
            >
              Annuler
            </button>
          </div>
          
          <div v-if="message" :class="messageType === 'success' ? 'text-green-600' : 'text-red-600'" class="text-sm">
            {{ message }}
          </div>
        </form>
      </div>

      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-xl font-bold mb-4">Gestion des documents</h2>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Télécharger un document
          </label>
          <div class="flex gap-2">
            <input
              id="documentFile"
              type="file"
              @change="handleDocumentUpload"
              accept=".pdf,.doc,.docx,.xls,.xlsx,.txt"
              class="flex-1 px-4 py-2 border border-gray-300 rounded-lg"
            />
            <button
              type="button"
              @click="uploadDocument"
              :disabled="!selectedDocument || isUploadingDoc"
              class="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors disabled:opacity-50"
            >
              {{ isUploadingDoc ? 'Envoi...' : 'Envoyer' }}
            </button>
          </div>
          <p class="text-xs text-gray-500 mt-1">
            Formats acceptés : PDF, DOC, DOCX, XLS, XLSX, TXT
          </p>
        </div>

        <div v-if="documentMessage" :class="documentMessageType === 'success' ? 'text-green-600' : 'text-red-600'" class="text-sm mb-4">
          {{ documentMessage }}
        </div>

        <div v-if="loadingDocuments" class="text-center py-4">
          <p class="text-gray-500">Chargement des documents...</p>
        </div>
        <div v-else-if="documents.length === 0" class="text-center py-4">
          <p class="text-gray-500">Aucun document</p>
        </div>
        <div v-else class="border rounded-lg overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Nom du fichier</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Taille</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="doc in documents" :key="doc.filename" class="hover:bg-gray-50">
                <td class="px-4 py-2 text-sm text-gray-900">{{ doc.filename }}</td>
                <td class="px-4 py-2 text-sm text-gray-500">{{ formatFileSize(doc.size) }}</td>
                <td class="px-4 py-2 text-sm font-medium">
                  <button
                    @click="insertDocumentLink(doc)"
                    class="text-blue-600 hover:text-blue-900 mr-3"
                    title="Insérer le lien dans l'article"
                  >
                    Insérer
                  </button>
                  <a
                    :href="getDocumentUrl(doc.url)"
                    target="_blank"
                    class="text-green-600 hover:text-green-900 mr-3"
                  >
                    Voir
                  </a>
                  <button
                    @click="deleteDocument(doc.filename)"
                    class="text-red-600 hover:text-red-900"
                  >
                    Supprimer
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-xl font-bold mb-4">Liste des actualités</h2>
        <div v-if="loading" class="text-center py-8">
          <p class="text-gray-500">Chargement...</p>
        </div>
        <div v-else-if="articles.length === 0" class="text-center py-8">
          <p class="text-gray-500">Aucune actualité</p>
        </div>
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Titre</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date de création</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="article in articles" :key="article.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">{{ article.titre }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-500">{{ formatDate(article.dateCreation) }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    @click="editArticle(article)"
                    class="text-blue-600 hover:text-blue-900 mr-4"
                  >
                    Modifier
                  </button>
                  <button
                    @click="deleteArticle(article.id)"
                    class="text-red-600 hover:text-red-900"
                  >
                    Supprimer
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <template #fallback>
      <div class="bg-white p-6 rounded-lg shadow">
        <PageHeader title="Gestion des actualités" />
        <div class="text-center py-8">
          <p class="text-gray-500">Chargement...</p>
        </div>
      </div>
    </template>
  </ClientOnly>
</template>

<script setup>
definePageMeta({
  middleware: 'admin',
  ssr: false
})

import { ref, onMounted } from 'vue'
import PageHeader from '~/components/PageHeader.vue'
import RichTextEditor from '~/components/RichTextEditor.vue'
import { useApi } from '~/composables/useApi'
import { useAuthStore } from '~/stores/auth'

const { apiFetch } = useApi()
const config = useRuntimeConfig()

const form = ref({
  titre: '',
  image: '',
  contenu: '',
  dateCreation: ''
})
const isSubmitting = ref(false)
const message = ref('')
const messageType = ref('')
const selectedArticle = ref(null)
const imageFile = ref(null)
const imagePreview = ref('')
const articles = ref([])
const loading = ref(false)

const documents = ref([])
const loadingDocuments = ref(false)
const selectedDocument = ref(null)
const isUploadingDoc = ref(false)
const documentMessage = ref('')
const documentMessageType = ref('')
const showDocumentsModal = ref(false)

const loadArticles = async () => {
  loading.value = true
  try {
    articles.value = await apiFetch('/articles')
  } catch (err) {
    console.error('Erreur lors du chargement des actualités:', err)
    message.value = 'Erreur lors du chargement des actualités'
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('fr-FR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatDateForInput = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day}T${hours}:${minutes}`
}

const editArticle = async (article) => {
  selectedArticle.value = article
  form.value = {
    titre: article.titre || '',
    image: article.image || '',
    contenu: article.contenu || '',
    dateCreation: formatDateForInput(article.dateCreation)
  }
  imageFile.value = null
  imagePreview.value = article.image || ''
  message.value = ''
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const resetForm = () => {
  selectedArticle.value = null
  form.value = {
    titre: '',
    image: '',
    contenu: '',
    dateCreation: ''
  }
  imageFile.value = null
  imagePreview.value = ''
  message.value = ''
}

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    message.value = 'Veuillez sélectionner un fichier image'
    messageType.value = 'error'
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    message.value = 'L\'image ne doit pas dépasser 5 Mo'
    messageType.value = 'error'
    return
  }

  imageFile.value = file
  const reader = new FileReader()
  
  reader.onload = (e) => {
    const base64 = e.target.result
    form.value.image = base64
    imagePreview.value = base64
  }
  
  reader.onerror = () => {
    message.value = 'Erreur lors de la lecture de l\'image'
    messageType.value = 'error'
  }
  
  reader.readAsDataURL(file)
}

const submitForm = async () => {
  isSubmitting.value = true
  message.value = ''
  
  const authStore = useAuthStore()
  
  if (process.client && !authStore.token) {
    const token = localStorage.getItem('token')
    if (token) {
      authStore.token = token
    }
  }
  
  if (!authStore.isAuthenticated) {
    message.value = 'Vous devez être connecté. Veuillez vous reconnecter.'
    messageType.value = 'error'
    isSubmitting.value = false
    if (process.client) {
      setTimeout(() => {
        window.location.href = '/'
      }, 2000)
    }
    return
  }
  
  try {
    let dateCreation = null
    if (form.value.dateCreation) {
      const date = new Date(form.value.dateCreation)
      dateCreation = date.toISOString()
    }
    
    const formData = {
      titre: form.value.titre,
      image: form.value.image,
      contenu: form.value.contenu,
      dateCreation: dateCreation
    }
    
    let response
    if (selectedArticle.value) {
      response = await apiFetch(`/articles/${selectedArticle.value.id}`, {
        method: 'PUT',
        body: formData
      })
      message.value = 'Actualité mise à jour avec succès'
    } else {
      response = await apiFetch('/articles', {
        method: 'POST',
        body: formData
      })
      message.value = 'Actualité enregistrée avec succès'
    }
    
    messageType.value = 'success'
    resetForm()
    await loadArticles()
  } catch (err) {
    console.error('Erreur complète:', err)
    const error = err || {}
    if (error.status === 401) {
      message.value = 'Session expirée. Veuillez vous reconnecter.'
    } else if (error.status === 403) {
      message.value = 'Accès refusé. Vérifiez que vous êtes connecté.'
    } else if (error.status === 413) {
      message.value = 'L\'image est trop volumineuse. Veuillez choisir une image plus petite (max 5 Mo).'
    } else if (error.status === 500) {
      const errorMessage = error.data?.message || error.message || 'Erreur serveur'
      message.value = `Erreur serveur: ${errorMessage}. Vérifiez les logs du backend.`
      console.error('Détails de l\'erreur 500:', error.data)
    } else if (error.status === 0 || (error.message && error.message.includes('Failed to fetch'))) {
      message.value = 'Impossible de contacter le serveur. Vérifiez que le backend est démarré.'
    } else {
      message.value = (error.data && error.data.message) || error.message || 'Erreur lors de l\'enregistrement'
    }
    messageType.value = 'error'
  } finally {
    isSubmitting.value = false
  }
}

const deleteArticle = async (id) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer cette actualité ?')) {
    return
  }
  
  try {
    await apiFetch(`/articles/${id}`, {
      method: 'DELETE'
    })
    message.value = 'Actualité supprimée avec succès'
    messageType.value = 'success'
    await loadArticles()
  } catch (err) {
    console.error('Erreur lors de la suppression:', err)
    message.value = 'Erreur lors de la suppression de l\'actualité'
    messageType.value = 'error'
  }
}

const loadDocuments = async () => {
  loadingDocuments.value = true
  try {
    documents.value = await apiFetch('/documents')
  } catch (err) {
    console.error('Erreur lors du chargement des documents:', err)
  } finally {
    loadingDocuments.value = false
  }
}

const handleDocumentUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedDocument.value = file
    documentMessage.value = ''
  }
}

const uploadDocument = async () => {
  if (!selectedDocument.value) return
  
  isUploadingDoc.value = true
  documentMessage.value = ''
  
  const authStore = useAuthStore()
  
  if (!authStore.token) {
    documentMessage.value = 'Session expirée. Veuillez vous reconnecter.'
    documentMessageType.value = 'error'
    isUploadingDoc.value = false
    return
  }
  
  try {
    const formData = new FormData()
    formData.append('file', selectedDocument.value)
    
    const response = await fetch(`${config.public.apiBase}/documents/upload`, {
      method: 'POST',
      body: formData,
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    
    if (!response.ok) {
      const errorData = await response.json()
        .catch(() => ({ error: 'Erreur inconnue' }))
      throw new Error(errorData.error || 'Erreur lors de l\'upload')
    }
    
    documentMessage.value = 'Document téléchargé avec succès'
    documentMessageType.value = 'success'
    selectedDocument.value = null
    document.getElementById('documentFile').value = ''
    await loadDocuments()
  } catch (err) {
    console.error('Erreur Upload:', err)
    documentMessage.value = `Erreur lors du téléchargement: ${err.message}`
    documentMessageType.value = 'error'
  } finally {
    isUploadingDoc.value = false
  }
}

const deleteDocument = async (filename) => {
  if (!confirm(`Supprimer le document "${filename}" ?`)) {
    return
  }
  
  try {
    await apiFetch(`/documents/${filename}`, {
      method: 'DELETE'
    })
    documentMessage.value = 'Document supprimé'
    documentMessageType.value = 'success'
    await loadDocuments()
  } catch (err) {
    console.error('Erreur suppression:', err)
    documentMessage.value = 'Erreur lors de la suppression'
    documentMessageType.value = 'error'
  }
}

const insertDocumentLink = (doc) => {
  const url = getDocumentUrl(doc.url)
  const linkHtml = `<a href="${url}" target="_blank">${doc.filename}</a>`
  form.value.contenu += linkHtml
  documentMessage.value = 'Lien inséré dans le contenu'
  documentMessageType.value = 'success'
  setTimeout(() => {
    documentMessage.value = ''
  }, 2000)
}

const getDocumentUrl = (url) => {
  return `${config.public.apiBase}${url}`
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

onMounted(() => {
  loadArticles()
  loadDocuments()
})
</script>
