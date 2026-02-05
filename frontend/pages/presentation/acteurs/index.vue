<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <PageHeader title="Acteurs du GFZ" />
    
    <div class="container-map relative">
      <div id="map" class="map relative">
        <img 
          src="https://gfz-online.fr/images/annuaire/carte-GFZ.png" 
          alt="Carte de France - Acteurs du GFZ" 
          style="width: 100%; height: auto;"
        />
        
        <!-- Montpellier -->
        <div class="absolute map-marker-montpellier" style="left: 60%; top: 77%;">
          <button 
            @click="toggleMarker('montpellier')"
            class="w-4 h-4 #000000 rounded-full cursor-pointer relative z-10"
          >
            <div class="w-4 h-4 bg-black rounded-full"></div>
          </button>
          <div 
            v-if="activeMarker === 'montpellier'"
            class="absolute bottom-full left-0 mb-2 bg-white shadow-lg p-4 rounded min-w-[300px] z-20 border border-gray-200"
          >
            <header class="mb-2">
              <h2 class="font-bold text-lg">Montpellier</h2>
            </header>
            <p class="mb-2">
              <NuxtLink to="/presentation/acteurs/icgm" class="text-blue-600 hover:underline">
                <strong>ICGM (Institut Charles Gerhardt Montpellier)</strong><br />
                <img src="https://gfz-online.fr/images/annuaire/logo-icgm.jpg" alt="ICGM" class="w-24 h-12 float-left mr-2" />
                Voir fiche
              </NuxtLink>
            </p>
            <hr class="my-2" />
            <p>
              <NuxtLink to="#" class="text-blue-600 hover:underline">
                <strong>SOMEZ, Saint-Jean-de-Védas</strong><br />
                Voir fiche
              </NuxtLink>
            </p>
          </div>
        </div>
        
        <!-- Marseille -->
        <div class="absolute map-marker-marseille" style="left: 77%; top: 77%;">
          <button 
            @click="toggleMarker('marseille')"
            class="w-4 h-4 #000000 rounded-full cursor-pointer relative z-10"
          >
            <div class="w-4 h-4 bg-black rounded-full"></div>
          </button>
          <div 
            v-if="activeMarker === 'marseille'"
            class="absolute bottom-full left-0 mb-2 bg-white shadow-lg p-4 rounded min-w-[300px] z-20 border border-gray-200"
          >
            <header class="mb-2">
              <h2 class="font-bold text-lg">Marseille</h2>
            </header>
            <p>
              <NuxtLink to="/presentation/acteurs/madirel" class="text-blue-600 hover:underline">
                <strong>MADIREL (Matériaux Divisés, Interfaces, Réactivité, ÉLectrochimie)</strong><br />
                <img src="https://gfz-online.fr/images/annuaire/logo-madirel.jpg" alt="MADIREL" class="w-24 h-10 float-left mr-2" />
                Voir fiche
              </NuxtLink>
            </p>
          </div>
        </div>
        
        <!-- Lyon -->
        <div class="absolute map-marker-lyon" style="left: 72%; top: 47%;">
          <button 
            @click="toggleMarker('lyon')"
            class="w-4 h-4 #000000 rounded-full cursor-pointer relative z-10"
          >
            <div class="w-4 h-4 bg-black rounded-full"></div>
          </button>
          <div 
            v-if="activeMarker === 'lyon'"
            class="absolute bottom-full left-0 mb-2 bg-white shadow-lg p-4 rounded min-w-[300px] z-20 border border-gray-200"
          >
            <header class="mb-2">
              <h2 class="font-bold text-lg">Lyon</h2>
            </header>
            <p class="mb-2">
              <NuxtLink to="/presentation/acteurs/ifpen" class="text-blue-600 hover:underline">
                <strong>IFPEN (IFP Energies Nouvelles)</strong><br />
                <img src="https://gfz-online.fr/images/annuaire/logo-ifpen.jpg" alt="IFPEN" class="w-24 h-10 float-left mr-2" />
                Voir fiche
              </NuxtLink>
            </p>
            <hr class="my-2" />
            <p>
              <NuxtLink to="/presentation/acteurs/irce" class="text-blue-600 hover:underline">
                <strong>IRCE (Institut de recherches sur la catalyse et l'environnement de Lyon)</strong><br />
                <img src="https://gfz-online.fr/images/annuaire/logo-irce.jpg" alt="IRCE" class="w-24 h-8 float-left mr-2" />
                Voir fiche
              </NuxtLink>
            </p>
          </div>
        </div>
        
        <!-- Mulhouse -->
        <div class="absolute map-marker-mulhouse" style="left: 84%; top: 28%;">
          <button 
            @click="toggleMarker('mulhouse')"
            class="w-4 h-4 #000000 rounded-full cursor-pointer relative z-10"
          >
            <div class="w-4 h-4 bg-black rounded-full"></div>
          </button>
          <div 
            v-if="activeMarker === 'mulhouse'"
            class="absolute bottom-full left-0 mb-2 bg-white shadow-lg p-4 rounded min-w-[300px] z-20 border border-gray-200"
          >
            <header class="mb-2">
              <h2 class="font-bold text-lg">Mulhouse</h2>
            </header>
            <p>
              <NuxtLink to="/presentation/acteurs/is2m" class="text-blue-600 hover:underline">
                <strong>IS2M (Institut de science des Matériaux de Mulhouse)</strong><br />
                <img src="https://gfz-online.fr/images/annuaire/logo-is2m.jpg" alt="IS2M" class="w-16 h-11 float-left mr-2" />
                Voir fiche
              </NuxtLink>
            </p>
          </div>
        </div>
        
        <!-- Lille -->
        <div class="absolute map-marker-lille" style="left: 54%; top: 7%;">
          <button 
            @click="toggleMarker('lille')"
            class="w-4 h-4 #000000 rounded-full cursor-pointer relative z-10"
          >
            <div class="w-4 h-4 bg-black rounded-full"></div>
          </button>
          <div 
            v-if="activeMarker === 'lille'"
            class="absolute bottom-full left-0 mb-2 bg-white shadow-lg p-4 rounded min-w-[300px] z-20 border border-gray-200"
          >
            <header class="mb-2">
              <h2 class="font-bold text-lg">Lille</h2>
            </header>
            <p>
              <NuxtLink to="/presentation/acteurs/lasir" class="text-blue-600 hover:underline">
                <strong>LASIR (LAboratoire de Spectrochimie Infrarouge et Raman), Villeneuve d'Ascq</strong><br />
                <img src="https://gfz-online.fr/images/annuaire/logo-lasir.jpg" alt="LASIR" class="w-24 h-10 float-left mr-2" />
                Voir fiche
              </NuxtLink>
            </p>
          </div>
        </div>
        
        <!-- Caen -->
        <div class="absolute map-marker-caen" style="left: 35%; top: 17%;">
          <button 
            @click="toggleMarker('caen')"
            class="w-4 h-4 #000000 rounded-full cursor-pointer relative z-10"
          >
            <div class="w-4 h-4 bg-black rounded-full"></div>
          </button>
          <div 
            v-if="activeMarker === 'caen'"
            class="absolute bottom-full left-0 mb-2 bg-white shadow-lg p-4 rounded min-w-[300px] z-20 border border-gray-200"
          >
            <header class="mb-2">
              <h2 class="font-bold text-lg">Caen</h2>
            </header>
            <p>
              <NuxtLink to="/presentation/acteurs/lcs" class="text-blue-600 hover:underline">
                <strong>LCS (Laboratoire Catalyse et Spectrochimie)</strong><br />
                <img src="https://gfz-online.fr/images/annuaire/logo-lcs.jpg" alt="LCS" class="w-14 h-12 float-left mr-2" />
                Voir fiche
              </NuxtLink>
            </p>
          </div>
        </div>
        
        <!-- Honfleur -->
        <div class="absolute map-marker-honfleur" style="left: 38%; top: 15%;">
          <button 
            @click="toggleMarker('honfleur')"
            class="w-4 h-4 #000000 rounded-full cursor-pointer relative z-10"
          >
            <div class="w-4 h-4 bg-black rounded-full"></div>
          </button>
          <div 
            v-if="activeMarker === 'honfleur'"
            class="absolute bottom-full left-0 mb-2 bg-white shadow-lg p-4 rounded min-w-[300px] z-20 border border-gray-200"
          >
            <header class="mb-2">
              <h2 class="font-bold text-lg">Honfleur</h2>
            </header>
            <p>
              <NuxtLink to="/presentation/acteurs/arkema" class="text-blue-600 hover:underline">
                <strong>ARKEMA – CECA, HONFLEUR</strong><br />
                Voir fiche
              </NuxtLink>
            </p>
          </div>
        </div>
        
        <!-- Lacq -->
        <div class="absolute map-marker-lacq" style="left: 22%; top: 77%;">
          <button 
            @click="toggleMarker('lacq')"
            class="w-4 h-4 #000000 rounded-full cursor-pointer relative z-10"
          >
            <div class="w-4 h-4 bg-black rounded-full"></div>
          </button>
          <div 
            v-if="activeMarker === 'lacq'"
            class="absolute bottom-full left-0 mb-2 bg-white shadow-lg p-4 rounded min-w-[300px] z-20 border border-gray-200"
          >
            <header class="mb-2">
              <h2 class="font-bold text-lg">Lacq</h2>
            </header>
            <p>
              <NuxtLink to="/presentation/acteurs/grl" class="text-blue-600 hover:underline">
                <strong>GROUPEMENT DE RECHERCHE DE LACQ</strong><br />
                Voir fiche
              </NuxtLink>
            </p>
          </div>
        </div>
        
        <!-- Paris -->
        <div class="absolute map-marker-paris" style="left: 50%; top: 22%;">
          <button 
            @click="toggleMarker('paris')"
            class="w-4 h-4 #000000 rounded-full cursor-pointer relative z-10"
          >
            <div class="w-4 h-4 bg-black rounded-full"></div>
          </button>
          <div 
            v-if="activeMarker === 'paris'"
            class="absolute bottom-full left-0 mb-2 bg-white shadow-lg p-4 rounded min-w-[300px] z-20 border border-gray-200"
          >
            <header class="mb-2">
              <h2 class="font-bold text-lg">Paris</h2>
            </header>
            <p class="mb-2">
              <NuxtLink to="/presentation/acteurs/impp" class="text-blue-600 hover:underline">
                <strong>Institut des Matériaux Poreux de Paris</strong><br />
                Voir fiche
              </NuxtLink>
            </p>
            <hr class="my-2" />
            <p>
              <NuxtLink to="/presentation/acteurs/lrs-upmc" class="text-blue-600 hover:underline">
                <strong>LRS (Laboratoire de Réactivité de Surface)</strong><br />
                <img src="https://gfz-online.fr/images/annuaire/logo-lrs.jpg" alt="LRS" class="w-24 h-11 float-left mr-2" />
                Voir fiche
              </NuxtLink>
            </p>
          </div>
        </div>
        
        <!-- Poitiers -->
        <div class="absolute map-marker-poitiers" style="left: 36%; top: 45%;">
          <button 
            @click="toggleMarker('poitiers')"
            class="w-4 h-4 #000000 rounded-full cursor-pointer relative z-10"
          >
            <div class="w-4 h-4 bg-black rounded-full"></div>
          </button>
          <div 
            v-if="activeMarker === 'poitiers'"
            class="absolute bottom-full left-0 mb-2 bg-white shadow-lg p-4 rounded min-w-[300px] z-20 border border-gray-200"
          >
            <header class="mb-2">
              <h2 class="font-bold text-lg">Poitiers</h2>
            </header>
            <p>
              <NuxtLink to="/presentation/acteurs/ic2mp" class="text-blue-600 hover:underline">
                <strong>IC2MP (Institut de Chimie des Milieux et Matériaux de Poitiers)</strong><br />
                <img src="https://gfz-online.fr/images/annuaire/logo-ic2mp.jpg" alt="IC2MP" class="w-12 h-12 float-left mr-2" />
                Voir fiche
              </NuxtLink>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import PageHeader from '~/components/PageHeader.vue'

const activeMarker = ref(null)

const toggleMarker = (marker) => {
  if (activeMarker.value === marker) {
    activeMarker.value = null
  } else {
    activeMarker.value = marker
  }
}

const handleClickOutside = (event) => {
  if (!event.target.closest('.map-marker-montpellier') && 
      !event.target.closest('.map-marker-marseille') &&
      !event.target.closest('.map-marker-lyon') &&
      !event.target.closest('.map-marker-mulhouse') &&
      !event.target.closest('.map-marker-lille') &&
      !event.target.closest('.map-marker-caen') &&
      !event.target.closest('.map-marker-honfleur') &&
      !event.target.closest('.map-marker-lacq') &&
      !event.target.closest('.map-marker-paris') &&
      !event.target.closest('.map-marker-poitiers')) {
    activeMarker.value = null
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.container-map {
  position: relative;
  width: 100%;
}

.map {
  position: relative;
  width: 100%;
}

.map-marker-montpellier,
.map-marker-marseille,
.map-marker-lyon,
.map-marker-mulhouse,
.map-marker-lille,
.map-marker-caen,
.map-marker-honfleur,
.map-marker-lacq,
.map-marker-paris,
.map-marker-poitiers {
  position: absolute;
  transform: translate(-50%, -50%);
}
</style>
