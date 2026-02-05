<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <PageHeader title="Identifiant oublié" />
    
    <div class="mt-6 max-w-md mx-auto">
      <p class="text-gray-700 mb-6">
        Si vous avez oublié votre identifiant, veuillez contacter l'administrateur 
        en utilisant le formulaire de contact ou en envoyant un email à l'adresse 
        de contact du site.
      </p>
      
      <div class="space-y-4">
        <NuxtLink
          to="/contact"
          class="block w-full bg-secondary text-white text-center py-2 px-4 rounded-lg hover:bg-secondary/90 transition"
        >
          Accéder au formulaire de contact
        </NuxtLink>
        
        <NuxtLink
          to="/"
          class="block w-full text-center text-secondary hover:text-secondary/80 transition"
        >
          Retour à l'accueil
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import PageHeader from '~/components/PageHeader.vue'
</script>
