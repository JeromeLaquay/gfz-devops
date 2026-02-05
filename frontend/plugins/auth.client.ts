export default defineNuxtPlugin(() => {
  const authStore = useAuthStore()
  
  if (process.client) {
    const token = localStorage.getItem('token')
    const userStr = localStorage.getItem('user')
    
    if (token) {
      authStore.token = token
    }
    
    if (userStr) {
      try {
        authStore.user = JSON.parse(userStr)
      } catch (e) {
        console.error('Erreur lors du parsing des données utilisateur:', e)
      }
    }
  }
})
