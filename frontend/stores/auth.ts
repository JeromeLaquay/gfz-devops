import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null as string | null,
    user: null as any | null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token
  },

  actions: {
    async login(credentials: { username: string; password: string }) {
      const config = useRuntimeConfig()
      const response = await $fetch(`${config.public.apiBase}/auth/login`, {
        method: 'POST',
        body: credentials
      })
      
      this.token = response.token
      this.user = response.user
      
      if (process.client) {
        localStorage.setItem('token', this.token)
        localStorage.setItem('user', JSON.stringify(this.user))
      }
      
      return response
    },

    logout() {
      this.token = null
      this.user = null
      if (process.client) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
      }
    }
  }
})
