<template>
  <div class="page-header mb-6">
    <h1 class="flex items-start" style="align-items: center;">
      <span class="bg-secondary w-16 h-16 flex items-center justify-center mr-3 flex-shrink-0">
        <i class="fa fa-thumb-tack text-white text-2xl"></i>
      </span>
      <span class="text-2xl font-normal text-gray-800 leading-tight mt-2">
        {{ title }}
      </span>
    </h1>
    <hr class="border-t-2 border-gray-300 mt-4">
  </div>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  }
})
</script>