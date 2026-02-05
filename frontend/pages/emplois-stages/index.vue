<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <PageHeader title="Emplois & Stages" />
    
    <div class="space-y-6 mt-6">
      <article 
        v-for="offre in offres" 
        :key="offre.id"
        class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
      >
        <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
          <div class="flex-1">
            <h2 class="text-xl font-semibold text-dark mb-3">
              {{ offre.titre }}
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
              <div v-if="offre.type" class="flex items-center text-gray-700">
                <i class="fa fa-briefcase text-secondary mr-2"></i>
                <span class="text-sm">{{ offre.type }}</span>
              </div>
              
              <div v-if="offre.localisation" class="flex items-center text-gray-700">
                <i class="fa fa-map-marker text-secondary mr-2"></i>
                <span class="text-sm">{{ offre.localisation }}</span>
              </div>
              
              <div v-if="offre.duree" class="flex items-center text-gray-700">
                <i class="fa fa-clock-o text-secondary mr-2"></i>
                <span class="text-sm">{{ offre.duree }}</span>
              </div>
              
              <div v-if="offre.dateExpiration" class="flex items-center text-gray-700">
                <i class="fa fa-calendar text-secondary mr-2"></i>
                <span class="text-sm">Expire le {{ offre.dateExpiration }}</span>
              </div>
            </div>
            
            <div v-if="offre.resume" class="text-gray-700 mb-4">
              <p class="line-clamp-3">{{ offre.resume }}</p>
            </div>
          </div>
        </div>
      </article>
      
      <div v-if="offres.length === 0 && !loading" class="text-center py-12 text-gray-500">
        <p>Aucune offre d'emploi ou de stage disponible pour le moment.</p>
      </div>
      
      <div v-if="loading" class="text-center py-12 text-gray-500">
        <p>Chargement des offres...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PageHeader from '~/components/PageHeader.vue'

const offres = ref([])
const loading = ref(true)

const formaterDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const chargerOffres = async () => {
  try {
    loading.value = true
    const { apiFetch } = useApi()
    const offresData = await apiFetch('/offres-emploi/valides')
    
    offres.value = offresData.map((offre) => ({
      id: offre.id,
      titre: offre.titre,
      type: offre.type,
      localisation: offre.localisation,
      duree: offre.duree,
      dateExpiration: formaterDate(offre.dateExpiration),
      resume: offre.resume
    }))
  } catch (error) {
    console.error('Erreur lors du chargement des offres:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  chargerOffres()
})
</script>
