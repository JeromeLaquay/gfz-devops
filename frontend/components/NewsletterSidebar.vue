<template>
  <div class="bg-white rounded-lg shadow">
    <div class="bg-[#376299] px-4 py-2 border-b-2 border-secondary">
      <h3 class="text-white font-semibold uppercase">INSCRIPTION NEWSLETTER</h3>
    </div>
    <form @submit.prevent="handleSubscribe" class="p-4 space-y-3">
      <input
        v-model="form.name"
        type="text"
        placeholder="Nom"
        required
        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-secondary"
      />
      <input
        v-model="form.email"
        type="email"
        placeholder="E-mail"
        required
        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-secondary"
      />
      <input
        v-model="form.emailConfirm"
        type="email"
        placeholder="Confirmation de l'e-mail"
        required
        class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-secondary"
      />
      <button
        type="submit"
        class="w-full bg-secondary text-white py-2 rounded hover:opacity-90 transition"
      >
        S'abonner
      </button>
      <button
        type="button"
        @click="handleUnsubscribe"
        class="w-full bg-gray-400 text-white py-2 rounded hover:bg-gray-500 transition"
      >
        Se désabonner
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const form = ref({
  name: '',
  email: '',
  emailConfirm: ''
})

const handleSubscribe = async () => {
  if (form.value.email !== form.value.emailConfirm) {
    alert('Les emails ne correspondent pas')
    return
  }
  
  try {
    const { apiFetch } = useApi()
    await apiFetch('/newsletter/subscribe', {
      method: 'POST',
      body: {
        name: form.value.name,
        email: form.value.email
      }
    })
    alert('Inscription réussie !')
    form.value = { name: '', email: '', emailConfirm: '' }
  } catch (error) {
    alert('Erreur lors de l\'inscription')
  }
}

const handleUnsubscribe = async () => {
  if (!form.value.email) {
    alert('Veuillez entrer votre email')
    return
  }
  
  try {
    const { apiFetch } = useApi()
    await apiFetch(`/newsletter/unsubscribe?email=${form.value.email}`, {
      method: 'POST'
    })
    alert('Désinscription réussie !')
    form.value = { name: '', email: '', emailConfirm: '' }
  } catch (error) {
    alert('Erreur lors de la désinscription')
  }
}
</script>
