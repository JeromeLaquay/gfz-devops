<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <PageHeader title="Réunion GFZ 2021" />
    
    <div class="text-gray-700 space-y-6 mt-6" style="text-align: center;">
      <div class="space-y-4">
        <p class="text-red-600" style="font-size: 14pt; font-family: 'Times New Roman', serif;">
          <strong>
            En raison de la pandémie de COVID-19, la 36<sup>ème</sup> 
            <strong>réunion annuelle du GFZ</strong> se tiendra en distanciel
          </strong>
        </p>
        
        <p style="font-size: 14pt; font-family: 'Times New Roman', serif;">
          <strong>
            sous la forme de <span class="text-red-600">webinaires</span> les matinées du 
            <span class="text-red-600"><strong>30 mars au 1<sup>er</sup> avril 2021</strong></span>.
          </strong>
        </p>
        
        <p style="font-size: 14pt; font-family: 'Times New Roman', serif;">
          <strong>
            Prenez soin de vous et de vos proches. Bon courage à tous.
          </strong>
        </p>
      </div>
      
      <div class="space-y-4 mt-8">
        <p>
          <a 
            href="/Troisime-circulaire_GFZ2021_2.pdf" 
            target="_blank"
            class="inline-block bg-secondary hover:bg-secondary-dark text-white font-semibold py-2 px-6 rounded-lg transition-colors"
          >
            Télécharger la circulaire
          </a>
        </p>
        
        <p>
          <a 
            href="/Fascicule.pdf" 
            target="_blank"
            class="inline-block bg-secondary hover:bg-secondary-dark text-white font-semibold py-2 px-6 rounded-lg transition-colors"
          >
            Télécharger le programme complet
          </a>
        </p>
      </div>
      
      <div class="space-y-6 mt-12">
        <div>
          <h2 class="text-xl font-bold mb-4" style="font-size: 14pt;">
            <strong>THÉMATIQUES</strong>
          </h2>
          <ul class="space-y-2">
            <li>Synthèse et mise en forme</li>
            <li>Applications</li>
            <li>Caractérisations et modélisation</li>
          </ul>
        </div>
        
        <div>
          <h2 class="text-xl font-bold mb-4" style="font-size: 14pt;">
            <strong>PROGRAMME</strong>
          </h2>
          <ul class="space-y-2">
            <li>Communications orales (10 min)</li>
            <li>Présentations des exposants</li>
            <li>Remise du quatrième et du cinquième prix de thèse Denise Barthomeuf du GFZ</li>
            <li>Prix de la meilleure communication</li>
          </ul>
        </div>
        
        <div>
          <h3 class="text-lg font-semibold mb-3 underline">
            <strong>Conférences plénières avec la participation confirmée de :</strong>
          </h3>
          <ul class="space-y-2">
            <li>Valentin Valtchev (LCS)</li>
            <li>Ovidiu Ersen (IPCMS)</li>
          </ul>
        </div>
        
        <div>
          <h3 class="text-lg font-semibold mb-3 underline">
            <strong>Keynote avec la participation confirmée de :</strong>
          </h3>
          <ul class="space-y-2">
            <li>Florian Wisser (IRCE Lyon / Universität Regensburg)</li>
            <li>Rémy Guillet-Nicolas (LCS)</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import PageHeader from '~/components/PageHeader.vue'
</script>