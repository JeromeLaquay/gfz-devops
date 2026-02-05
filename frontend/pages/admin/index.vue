<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <PageHeader title="Administration" />
    
    <div class="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <NuxtLink
        to="/admin/actualites"
        class="block p-6 border-2 border-gray-200 rounded-lg hover:border-secondary transition-colors"
      >
        <h3 class="text-xl font-semibold text-dark mb-2">Actualités</h3>
        <p class="text-gray-600">Ajouter et gérer les actualités</p>
      </NuxtLink>
      
      <NuxtLink
        to="/admin/offres-emploi"
        class="block p-6 border-2 border-gray-200 rounded-lg hover:border-secondary transition-colors"
      >
        <h3 class="text-xl font-semibold text-dark mb-2">Offres d'emploi</h3>
        <p class="text-gray-600">Ajouter des offres d'emploi</p>
      </NuxtLink>
      
      <NuxtLink
        to="/admin/contact"
        class="block p-6 border-2 border-gray-200 rounded-lg hover:border-secondary transition-colors"
      >
        <h3 class="text-xl font-semibold text-dark mb-2">Messages</h3>
        <p class="text-gray-600">Consulter les messages de contact</p>
      </NuxtLink>
      
      <NuxtLink
        to="/admin/newsletters"
        class="block p-6 border-2 border-gray-200 rounded-lg hover:border-secondary transition-colors"
      >
        <h3 class="text-xl font-semibold text-dark mb-2">Newsletters</h3>
        <p class="text-gray-600">Gérer les newsletters</p>
      </NuxtLink>
      
      <NuxtLink
        to="/admin/utilisateurs"
        class="block p-6 border-2 border-gray-200 rounded-lg hover:border-secondary transition-colors"
      >
        <h3 class="text-xl font-semibold text-dark mb-2">Utilisateurs</h3>
        <p class="text-gray-600">Gérer les administrateurs</p>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'admin'
})

import PageHeader from '~/components/PageHeader.vue'
</script>
