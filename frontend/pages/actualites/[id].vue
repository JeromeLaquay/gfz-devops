<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-500">Chargement de l'actualité...</p>
    </div>
    
    <div v-else-if="error" class="text-center py-12">
      <p class="text-red-500">{{ error }}</p>
      <NuxtLink to="/actualites" class="text-secondary hover:underline mt-4 inline-block">
        Retour aux actualités
      </NuxtLink>
    </div>
    
    <article v-else-if="actualite">
      <NuxtLink 
        to="/actualites" 
        class="inline-flex items-center text-secondary hover:underline mb-6"
      >
        <i class="fa fa-arrow-left mr-2"></i>
        Retour aux actualités
      </NuxtLink>
      
      <header class="mb-6">
        <h1 class="text-3xl font-bold text-dark mb-4">
          {{ actualite.titre }}
        </h1>
        <p class="text-sm text-gray-500">
          {{ actualite.date }}
        </p>
      </header>
      
      <div v-if="actualite.image" class="mb-6">
        <img 
          :src="actualite.image" 
          :alt="actualite.titre"
          class="w-full h-96 object-cover rounded-lg"
        />
      </div>
      
      <div 
        class="prose max-w-none text-gray-700"
        v-html="actualite.contenu"
      ></div>
    </article>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const route = useRoute()
const actualite = ref(null)
const loading = ref(true)
const error = ref(null)

const formaterDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const decoderHtml = (html) => {
  if (!html) return ''
  const txt = document.createElement('textarea')
  txt.innerHTML = html
  return txt.value
}

const chargerActualite = async () => {
  try {
    loading.value = true
    error.value = null
    const id = route.params.id
    const { apiFetch } = useApi()
    const article = await apiFetch(`/articles/${id}`)
    
    actualite.value = {
      titre: article.titre,
      image: article.image || null,
      contenu: decoderHtml(article.contenu || ''),
      date: formaterDate(article.dateCreation)
    }
  } catch (err) {
    error.value = 'Actualité introuvable ou erreur lors du chargement.'
    console.error('Erreur:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  chargerActualite()
})
</script>
