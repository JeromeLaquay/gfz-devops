<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <PageHeader title="Réunion GFZ 2019" />
    
    <div class="text-gray-700 space-y-6 mt-6" style="text-align: center;">
      <p style="font-size: 12pt; font-family: 'Times New Roman', serif;">
        <strong>
          Merci à tous d'avoir participé à la 35<sup>ème</sup> réunion annuelle du GFZ !
        </strong>
      </p>
      
      <div class="flex justify-center">
        <img 
          src="~/assets/Image_2019.jpg" 
          alt="Image 2019" 
          class="w-auto h-auto max-w-xs"
        />
      </div>
      
      <p style="font-size: 12pt; font-family: 'Times New Roman', serif;">
        <a 
          href="/Livret_Programme_GFZ2019.pdf" 
          target="_blank"
          class="text-blue-600 hover:underline inline-flex items-center"
        >
          <i class="fa fa-download mr-2"></i>
          Télécharger le programme scientifique détaillé
        </a>
      </p>
    </div>
  </div>
</template>

<script setup>
import PageHeader from '~/components/PageHeader.vue'
</script>
