<template>
  <div class="bg-white rounded-lg shadow">
    <div class="bg-[#376299] px-4 py-2 border-b-2 border-secondary">
      <h3 class="text-white font-semibold uppercase">RECHERCHER</h3>
    </div>
    <div class="p-4">
      <div class="flex">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Recherche..."
          class="flex-1 px-3 py-2 border border-gray-300 rounded-l focus:outline-none focus:ring-2 focus:ring-secondary"
          @keyup.enter="handleSearch"
        />
        <button
          @click="handleSearch"
          class="bg-secondary text-white px-4 py-2 rounded-r hover:opacity-90 transition"
        >
          🔍
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    // TODO: Implémenter la recherche
    console.log('Recherche:', searchQuery.value)
  }
}
</script>
