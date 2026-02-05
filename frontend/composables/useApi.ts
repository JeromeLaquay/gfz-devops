import { useAuthStore } from '~/stores/auth'

export const useApi = () => {
  const config = useRuntimeConfig()
  const authStore = useAuthStore()

  const apiFetch = async (url: string, options: any = {}) => {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...options.headers
    }

    if (authStore.token) {
      headers.Authorization = `Bearer ${authStore.token}`
    } else if (process.client) {
      console.warn('Aucun token d\'authentification trouvé pour la requête:', url)
    }

    if (process.client) {
      console.log('Requête API:', {
        url: `${config.public.apiBase}${url}`,
        method: options.method || 'GET',
        hasToken: !!authStore.token
      })
    }

    try {
      return await $fetch(`${config.public.apiBase}${url}`, {
        ...options,
        headers,
        timeout: 60000
      })
    } catch (error: any) {
      if (process.client) {
        console.error('Erreur API:', {
          url,
          status: error.status,
          message: error.message,
          hasToken: !!authStore.token
        })
      }
      if (error.status === 401 || error.status === 403) {
        if (authStore.isAuthenticated) {
          authStore.logout()
          if (process.client) {
            window.location.href = '/'
          }
        }
      }
      throw error
    }
  }

  return { apiFetch }
}
