<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <PageHeader title="Bienvenue sur le site web de l'association GFZ">
    </PageHeader>
    <div class="entry-content">
      <p class="mb-4">&nbsp;</p>
      
      <p class="text-center mb-3">
        <span style="font-family: arial, helvetica, sans-serif; font-size: 14pt;">
          <strong>The 41st <strong>annual meeting of the GFZ</strong> will take place</strong>
        </span>
      </p>
      
      <p class="text-center mb-3">
        <span style="font-family: arial, helvetica, sans-serif; font-size: 14pt;">
          <strong>from March 30 to April 2<sup>nd</sup> 2026</strong>
        </span>
      </p>
      
      <p class="text-center mb-3">
        <span style="font-family: arial, helvetica, sans-serif; font-size: 14pt;">
          <strong>at Village Vacances Port-Bail in Normandie, France</strong>
        </span>
      </p>
      
      <p class="text-center mb-3">
        <span style="font-size: 14pt;">
          <strong>
            <a 
              href="/PremierCirculaire-GFZ.pdf" 
              target="_blank"
              style="color: #0000ff;"
            >
              Download the 1st circular
            </a>
          </strong>
        </span>
      </p>
      
      <p class="text-center mb-3">
        <span style="font-size: 14pt;">
          You can now submit your abstract for oral communication or poster presentation
        </span>
      </p>
      
      <p class="text-center mb-3">
        <span style="font-family: 'arial black', 'avant garde';">
          <strong>
            <span style="font-size: 18pt;">
              <a 
                href="https://gfz-2026.sciencesconf.org/?lang=fr" 
                style="color: #0000ff;"
              >
                here
              </a>
            </span>
          </strong>
        </span>
      </p>
      
      <p class="text-center mb-3">
        <span style="font-family: arial, helvetica, sans-serif; font-size: 14pt;">
          <strong>Hope to see you in Port-Bail</strong>
        </span>
      </p>
      
      <p class="mb-4">&nbsp;</p>
    </div>
    
    <div v-if="actualites.length > 0" class="mt-8 pt-8 border-t border-gray-200">
      <h2 class="text-2xl font-semibold text-dark mb-6">Dernières actualités</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <article
          v-for="actualite in actualites"
          :key="actualite.id"
          class="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow"
        >
          <NuxtLink :to="actualite.lien" class="block">
            <div class="aspect-video bg-gray-200 overflow-hidden">
              <img
                v-if="actualite.image"
                :src="actualite.image"
                :alt="actualite.titre"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
                <span class="text-4xl">📄</span>
              </div>
            </div>
            <div class="p-4">
              <h3 class="text-lg font-semibold text-dark mb-2 line-clamp-2">
                {{ actualite.titre }}
              </h3>
              <p class="text-sm text-gray-500 mb-2">
                {{ actualite.date }}
              </p>
              <p class="text-gray-700 text-sm line-clamp-3">
                {{ actualite.extrait }}
              </p>
            </div>
          </NuxtLink>
        </article>
      </div>
      <div class="mt-6 text-center">
        <NuxtLink
          to="/actualites"
          class="inline-block text-secondary hover:text-secondary/80 font-semibold transition"
        >
          Voir toutes les actualités →
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

const actualites = ref([])

const formaterDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const decoderHtml = (html) => {
  if (!html) return ''
  if (typeof window === 'undefined') return html
  const txt = document.createElement('textarea')
  txt.innerHTML = html
  return txt.value
}

const extraireExtrait = (contenu, maxLength = 150) => {
  if (!contenu) return ''
  let texte = contenu.replace(/<[^>]*>/g, '')
  texte = decoderHtml(texte)
  if (texte.length <= maxLength) return texte
  return texte.substring(0, maxLength).trim() + '...'
}

const chargerDernieresActualites = async () => {
  try {
    const { apiFetch } = useApi()
    const articles = await apiFetch('/articles')
    
    const articlesTries = articles
      .sort((a, b) => {
        const dateA = new Date(a.dateCreation || 0)
        const dateB = new Date(b.dateCreation || 0)
        return dateB - dateA
      })
      .slice(0, 3)
    
    actualites.value = articlesTries.map((article) => ({
      id: article.id,
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
  chargerDernieresActualites()
})
</script>
