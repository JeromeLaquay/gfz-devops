/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#376299',
        // Secondary: #f7bf66 (orange/jaune)
        secondary: '#f7bf66',
        dark: '#1f2937',
        light: '#f3f4f6',
        'page-title': '#353535'
      }
    }
  },
  plugins: []
}
