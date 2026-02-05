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
          Institut des Matériaux Poreux de Paris
        </h1>
      </header>
      
      <div class="prose max-w-none text-gray-700 space-y-4">
        <p>
          L'Institut des Matériaux Poreux de Paris, créé fin 2016 et constitué d'anciens 
          membres de l'équipe solides poreux de l'Institut Lavoisier de Versailles, a pour 
          objectifs de développer de nouveaux matériaux poreux hybrides fonctionnels (MOFs), 
          leur mise à l'échelle et en forme pour des applications potentielles dans le domaine 
          de la santé, l'énergie et l'environnement.
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
  siteWeb: 'http://www.chimie.ens.fr/?q=fre-imap-2000',
  adresse: 'Institut des Matériaux Poreux de Paris\nFRE CNRS ENS-ESPCI\n24 rue Lhomond, 10 rue Vauquelin\n75005 Paris',
  telephone: '+33 (0) 6 83 95 02 30',
  email: 'christian.serre@ens.fr'
})

onMounted(() => {
  // Les données pourraient être chargées depuis le backend plus tard
})
</script>
