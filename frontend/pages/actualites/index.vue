<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <PageHeader title="Actualités" />
    
    <div class="space-y-6 mt-6">
      <article 
        v-for="(actualite, index) in actualites" 
        :key="index"
        class="border-b border-gray-200 pb-6 last:border-b-0"
      >
        <div class="flex flex-col md:flex-row gap-4">
          <div v-if="actualite.image" class="md:w-1/3 flex-shrink-0">
            <img 
              :src="actualite.image" 
              :alt="actualite.titre"
              class="w-full h-48 object-cover rounded-lg"
            />
          </div>
          <div :class="actualite.image ? 'md:w-2/3' : 'md:w-full'">
            <h2 class="text-xl font-semibold text-dark mb-2">
              <NuxtLink :to="actualite.lien" class="hover:text-secondary transition">
                {{ actualite.titre }}
              </NuxtLink>
            </h2>
            <p class="text-sm text-gray-500 mb-3">
              {{ actualite.date }}
            </p>
            <p class="text-gray-700">
              {{ actualite.extrait }}
            </p>
            <NuxtLink 
              :to="actualite.lien" 
              class="inline-block mt-3 text-secondary hover:underline font-semibold"
            >
              Lire la suite...
            </NuxtLink>
          </div>
        </div>
      </article>
      
      <div v-if="actualites.length === 0" class="text-center py-12 text-gray-500">
        <p>Aucune actualité disponible pour le moment.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PageHeader from '~/components/PageHeader.vue'

const actualites = ref([])

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

const extraireExtrait = (contenu, maxLength = 200) => {
  if (!contenu) return ''
  let texte = contenu.replace(/<[^>]*>/g, '')
  texte = decoderHtml(texte)
  if (texte.length <= maxLength) return texte
  return texte.substring(0, maxLength).trim() + '...'
}

const chargerActualites = async () => {
  try {
    const { apiFetch } = useApi()
    const articles = await apiFetch('/articles')
    
    actualites.value = articles.map((article) => ({
      titre: article.titre,
      image: article.image || null,
      date: formaterDate(article.dateCreation),
      extrait: extraireExtrait(article.contenu),
      lien: `/actualites/${article.id}`
    }))
  } catch (error) {
    console.error('Erreur lors du chargement des actualités:', error)
  }
}

onMounted(() => {
  chargerActualites()
})
</script>
