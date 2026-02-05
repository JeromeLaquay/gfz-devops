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
          IC2MP, Poitiers
        </h1>
        <p class="text-gray-600 text-lg">IC2MP</p>
      </header>
      
      <div class="prose max-w-none text-gray-700 space-y-4">
        <p>
          L'IC2MP ou Institut de Chimie des Milieux et Matériaux de Poitiers est un Institut 
          de recherche interdisciplinaire créé en 2012 (Directeur Sabine Petit), dans le domaine 
          de la chimie et des géosciences de surface. L'IC2MP dépend de deux tutelles: le CNRS 
          et l'Université de Poitiers (UMR CNRS 7285).
        </p>
        
        <p>
          L'Institut regroupe un effectif de 250 personnes. 100 chercheurs (75 enseignants-chercheurs 
          de l'université de Poitiers et 25 chercheurs du CNRS). 50 personnels permanents d'appui 
          à la recherche (26 universités et 24 CNRS). 86 doctorants et 14 post-doctorants et 
          personnels temporaires.
        </p>
        
        <p>
          Les domaines d'application concernent l'énergie, les matériaux et les ressources naturelles 
          dans le cadre d'un environnement durable et plus spécifiquement :
        </p>
        
        <ul class="list-disc list-inside space-y-2 ml-4">
          <li>l'efficacité des procédés (catalyse, recyclage, traitement de l'eau, molécules à haute valeur ajoutée…),</li>
          <li>la gestion durable des ressources (eaux, sols carbone, minerais, déchets, …),</li>
          <li>l'intégration de la chimie dans les filières d'avenir (matériaux biosourcées, stockage de l'énergie, …).</li>
        </ul>
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
          
          <div v-if="acteur.fax">
            <dt class="font-semibold">Fax. :</dt>
            <dd>{{ acteur.fax }}</dd>
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
  siteWeb: 'http://ic2mp.labo.univ-poitiers.fr/',
  adresse: 'IC2MP – UMR 7285\nUniversité de Poitiers – SFA\nBâtiments B27, B28 et B35\n4, rue Michel Brunet – TSA 51106,\n86073 Poitiers cedex 9',
  telephone: '+33 (0) 5 49 45 37 02',
  fax: '+33 (0) 5 49 45 34 99',
  email: 'secretariat.ic2mp@univ-poitiers.fr'
})

onMounted(() => {
  // Les données pourraient être chargées depuis le backend plus tard
})
</script>
