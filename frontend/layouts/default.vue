<template>
  <div class="min-h-screen bg-gray-50">
    <Header />
    <main class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div class="lg:col-span-3">
          <slot />
        </div>
        <div class="lg:col-span-1 space-y-6">
          <SearchSidebar />
          <NewsletterSidebar />
          <LoginSidebar />
        </div>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script setup>


</script>
