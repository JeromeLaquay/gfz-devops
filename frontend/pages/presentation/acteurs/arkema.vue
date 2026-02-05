<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <NuxtLink 
      to="/presentation/acteurs" 
      class="inline-flex items-center text-secondary hover:underline mb-6"
    >
      <i class="fa fa-arrow-left mr-2"></i>
      Retour aux acteurs du GFZ
    </NuxtLink>
    
    <article>
      <header class="mb-6">
        <h1 class="text-3xl font-bold text-dark mb-2">
          ARKEMA - CECA, Honfleur
        </h1>
        <p class="text-gray-600 text-lg">Unité de production de tamis moléculaires ARKEMA - CECA de Honfleur</p>
      </header>
      
      <div class="prose max-w-none text-gray-700 space-y-4">
        <p>
          L'usine de Honfleur produit 20 000 tonnes de tamis moléculaires chaque année. 
          Les équipes sont spécialisées dans les procédés physico-chimiques de fabrication 
          de tamis moléculaires.
        </p>
        
        <p>
          Avec environ 120 salariés, l'usine est le premier employeur de Honfleur.
        </p>
      </div>
      
      <div class="mt-8 pt-6 border-t border-gray-200">
        <h2 class="text-xl font-semibold text-dark mb-4">Informations de contact</h2>
        <dl class="space-y-3 text-gray-700">
          <div v-if="acteur.siteWeb">
            <dt class="font-semibold">Site web :</dt>
            <dd>
              <a :href="acteur.siteWeb" target="_blank" class="text-secondary hover:underline">
                {{ acteur.siteWeb }}
              </a>
            </dd>
          </div>
          
          <div v-if="acteur.adresse">
            <dt class="font-semibold">Adresse postale :</dt>
            <dd class="whitespace-pre-line">{{ acteur.adresse }}</dd>
          </div>
          
          <div v-if="acteur.telephone">
            <dt class="font-semibold">Tél. :</dt>
            <dd>{{ acteur.telephone }}</dd>
          </div>
          
          <div v-if="acteur.email">
            <dt class="font-semibold">Contact email :</dt>
            <dd>
              <a :href="`mailto:${acteur.email}`" class="text-secondary hover:underline">
                {{ acteur.email }}
              </a>
            </dd>
          </div>
        </dl>
      </div>
    </article>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const acteur = ref({
  siteWeb: '',
  adresse: '',
  telephone: '',
  email: ''
})

onMounted(() => {
  // Les données pourraient être chargées depuis le backend plus tard
  acteur.value = {
    siteWeb: '',
    adresse: '',
    telephone: '',
    email: ''
  }
})
</script>
