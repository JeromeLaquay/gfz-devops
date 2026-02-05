<template>
  <header class="bg-white shadow-sm sticky top-0 z-50">
    <div class="container mx-auto px-4 py-4">
      <div class="flex justify-between items-center">
        <div class="flex items-center flex-1">
          <h1 class="text-secondary text-xl font-bold uppercase hidden md:block">
            GROUPE FRANÇAIS DES ZÉOLITHES
          </h1>
          <h1 class="text-secondary text-sm font-bold uppercase md:hidden">
            GFZ
          </h1>
        </div>
        <div class="flex-1 flex justify-center">
          <NuxtLink to="/" class="flex items-center justify-center">
            <img 
              src="~/assets/gfz-logo.png" 
              alt="GFZ Logo" 
              class="h-20 w-auto object-contain"
            />
          </NuxtLink>
        </div>
        <div class="flex items-center space-x-2 md:space-x-4 flex-1 justify-end">
          <div v-if="isAuthenticated" class="hidden md:flex items-center space-x-2">
            <span class="text-gray-700 text-sm">
              Bonjour <span class="font-semibold text-secondary">{{ displayName }}</span>
            </span>
            <button 
              @click="handleLogout"
              class="text-sm text-gray-600 hover:text-secondary transition px-2 py-1 rounded"
            >
              Déconnexion
            </button>
          </div>
          <a href="https://www.facebook.com/gfzonline/" target="_blank" class="w-8 h-8 md:w-10 md:h-10 bg-[#3a589b] rounded-full flex items-center justify-center transition hover:opacity-80">
            <span class="text-white text-lg md:text-2xl font-bold">f</span>
          </a>
          <a href="https://www.linkedin.com/company/groupe-fran%C3%A7ais-des-z%C3%A9olithes-gfz/about/" target="_blank" class="w-8 h-8 md:w-10 md:h-10 bg-[#007ab9] rounded-full flex items-center justify-center transition hover:opacity-80">
            <span class="text-white text-lg md:text-2xl font-bold">in</span>
          </a>
          <button
            @click="toggleMenu"
            class="md:hidden w-10 h-10 flex flex-col justify-center items-center space-y-1.5 text-secondary"
            aria-label="Menu"
          >
            <span 
              :class="[
                'block w-6 h-0.5 bg-current transition-all duration-300',
                isMenuOpen ? 'rotate-45 translate-y-2' : ''
              ]"
            ></span>
            <span 
              :class="[
                'block w-6 h-0.5 bg-current transition-all duration-300',
                isMenuOpen ? 'opacity-0' : ''
              ]"
            ></span>
            <span 
              :class="[
                'block w-6 h-0.5 bg-current transition-all duration-300',
                isMenuOpen ? '-rotate-45 -translate-y-2' : ''
              ]"
            ></span>
          </button>
        </div>
      </div>
    </div>
    <nav 
      :class="[
        'bg-[#376299] relative w-full transition-all duration-300',
        'md:overflow-visible',
        isMenuOpen ? 'max-h-screen overflow-hidden' : 'max-h-0 overflow-hidden md:max-h-none'
      ]"
    >
      <div class="container mx-auto px-4 relative">
        <div v-if="isAuthenticated && isMobile" class="md:hidden py-3 border-b border-[#4a7ab8] mb-2">
          <div class="text-white text-sm mb-2">
            Bonjour <span class="font-semibold text-secondary">{{ displayName }}</span>
          </div>
          <button 
            @click="handleLogout"
            class="text-sm text-white hover:text-secondary transition px-2 py-1 rounded border border-white/30 hover:border-secondary"
          >
            Déconnexion
          </button>
        </div>
        <ul class="flex flex-col md:flex-row md:flex-wrap md:items-center md:justify-center gap-x-6 gap-y-2 py-3">
          <li 
            v-for="item in menuItems" 
            :key="item.name" 
            class="relative group"
            @mouseenter="handleMenuEnter(item)"
            @mouseleave="handleMenuLeave"
          >
            <div class="flex items-center justify-between md:block">
              <NuxtLink
                :to="item.path"
                :class="[
                  'text-white hover:text-secondary transition relative inline-block text-sm uppercase tracking-wide py-1 md:py-1',
                  isActive(item.path) ? 'text-secondary' : ''
                ]"
                @click="handleMenuClick(item)"
              >
                {{ item.name }}
                <span v-if="isActive(item.path)" 
                      class="absolute bottom-0 left-0 right-0 h-0.5 bg-secondary"></span>
              </NuxtLink>
              <button
                v-if="item.submenu && isMobile"
                @click="toggleSubmenu(item.name)"
                class="md:hidden text-white ml-2"
              >
                <i :class="['fa', expandedSubmenus.includes(item.name) ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
              </button>
            </div>
            <div 
              v-if="item.submenu && (
                (!isMobile && hoveredMenu === item.name) || 
                (isMobile && expandedSubmenus.includes(item.name))
              )"
              :class="[
                'md:absolute md:top-full md:left-1/2 md:-translate-x-1/2 md:pt-2 bg-transparent z-[100]',
                isMobile ? 'mt-2' : ''
              ]"
              @mouseenter="handleSubmenuEnter"
              @mouseleave="handleSubmenuLeave"
            >
              <div class="bg-white shadow-xl min-w-[220px] border border-gray-200 rounded-md">
                <NuxtLink
                  v-for="subItem in item.submenu"
                  :key="subItem.name"
                  :to="subItem.path"
                  :class="[
                    'block px-4 py-2 text-dark hover:bg-[#fef8f0] transition relative',
                    isActive(subItem.path) ? 'bg-[#fef8f0] text-secondary font-semibold' : ''
                  ]"
                  @click="handleSubmenuClick"
                >
                  {{ subItem.name }}
                  <span v-if="subItem.submenu" class="float-right text-secondary ml-2">→</span>
                </NuxtLink>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { storeToRefs } from 'pinia'

const route = useRoute()
const authStore = useAuthStore()
const hoveredMenu = ref(null)
const isMenuOpen = ref(false)
const expandedSubmenus = ref([])
const isMobile = ref(false)
const hoverTimeout = ref(null)

const { isAuthenticated, user } = storeToRefs(authStore)

const displayName = computed(() => {
  if (!user.value) return ''
  return user.value.name || user.value.username || 'Utilisateur'
})

const handleLogout = () => {
  authStore.logout()
  navigateTo('/')
}

const isActive = (path) => {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}

const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
  if (!isMobile.value) {
    isMenuOpen.value = false
    expandedSubmenus.value = []
  }
}

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
  if (!isMenuOpen.value) {
    expandedSubmenus.value = []
  }
}

const toggleSubmenu = (menuName) => {
  const index = expandedSubmenus.value.indexOf(menuName)
  if (index > -1) {
    expandedSubmenus.value.splice(index, 1)
  } else {
    expandedSubmenus.value.push(menuName)
  }
}

const handleMenuClick = (item) => {
  if (isMobile.value && !item.hasSubmenu) {
    isMenuOpen.value = false
  }
}

const handleSubmenuClick = () => {
  if (isMobile.value) {
    isMenuOpen.value = false
    expandedSubmenus.value = []
  }
}

const handleMenuEnter = (item) => {
  if (item.hasSubmenu && !isMobile.value) {
    if (hoverTimeout.value) {
      clearTimeout(hoverTimeout.value)
      hoverTimeout.value = null
    }
    hoveredMenu.value = item.name
  }
}

const handleMenuLeave = () => {
  if (!isMobile.value) {
    hoverTimeout.value = setTimeout(() => {
      hoveredMenu.value = null
    }, 200)
  }
}

const handleSubmenuEnter = () => {
  if (!isMobile.value) {
    if (hoverTimeout.value) {
      clearTimeout(hoverTimeout.value)
      hoverTimeout.value = null
    }
  }
}

const handleSubmenuLeave = () => {
  if (!isMobile.value) {
    hoverTimeout.value = setTimeout(() => {
      hoveredMenu.value = null
    }, 200)
  }
}

const menuItems = computed(() => {
  const items = [
    { 
      name: 'ACCUEIL', 
      path: '/', 
      hasSubmenu: false
    },
    { 
      name: 'PRÉSENTATION', 
      path: '/presentation/mot-du-president', 
      hasSubmenu: true,
      submenu: [
        { name: 'Mot du président', path: '/presentation/mot-du-president' },
        { name: 'Fonctionnement', path: '/presentation/fonctionnement' },
        { name: 'Acteurs du GFZ', path: '/presentation/acteurs', submenu: true }
      ]
    },
    { 
      name: 'SOLIDES POREUX', 
      path: '/solid-poreux/generalites', 
      hasSubmenu: true,
      submenu: [
        { name: 'Généralités', path: '/solid-poreux/generalites' },
        { name: 'Zéolithes', path: '/solid-poreux/zeolithes' },
        { name: 'MOFs', path: '/solid-poreux/mofs' },
        { name: 'Solides mésostructurés', path: '/solid-poreux/mesostructures' },
        { name: 'Vidéos', path: '/solid-poreux/videos' }
      ]
    },
    { 
      name: 'BOURSES / PRIX', 
      path: '/bourses-prix', 
      hasSubmenu: true,
      submenu: [
        { name: 'Prix de thèse GFZ', path: '/bourses-prix/prix-these' },
        { name: 'Prix jeune chercheur/chercheuse', path: '/bourses-prix/prix-jeune-chercheur' }
      ]
    },
    { 
      name: 'RÉUNIONS GFZ', 
      path: '/reunions/passees', 
      hasSubmenu: true,
      submenu: [
        { name: 'Réunions passées', path: '/reunions/passees' },
        { name: 'Réunion GFZ 2019', path: '/reunions/2019' },
        { name: 'Réunion GFZ 2021', path: '/reunions/2021' },
        { name: 'Réunion GFZ 2022', path: '/reunions/2022' },
        { name: 'Réunion GFZ 2023', path: '/reunions/2023' },
        { name: 'Réunion GFZ 2024', path: '/reunions/2024' }
      ]
    },
    { 
      name: 'EMPLOIS & STAGES', 
      path: '/emplois-stages', 
      hasSubmenu: false
    },
    { 
      name: 'LIENS', 
      path: '/liens', 
      hasSubmenu: false
    },
    { 
      name: 'CONTACT', 
      path: '/contact', 
      hasSubmenu: false
    },
    { 
      name: 'ACTUALITÉS', 
      path: '/actualites', 
      hasSubmenu: false
    }
  ]

  if (isAuthenticated.value) {
    items.push({
      name: 'ADMIN',
      path: '/admin',
      hasSubmenu: true,
      submenu: [
        { name: 'Ajouter une actualité', path: '/admin/actualites' },
        { name: 'Ajouter une newsletter', path: '/admin/newsletters' },
        { name: 'Ajouter une offre d\'emploi', path: '/admin/offres-emploi' },
        { name: 'Consulter les messages', path: '/admin/contact' },
        { name: 'Gérer les administrateurs', path: '/admin/utilisateurs' }
      ]
    })
  }

  return items
})

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
  if (hoverTimeout.value) {
    clearTimeout(hoverTimeout.value)
  }
})
</script>
