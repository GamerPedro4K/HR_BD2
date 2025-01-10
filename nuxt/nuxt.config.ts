// https://nuxt.com/docs/api/configuration/nuxt-config
import Aura from '@primevue/themes/aura';



export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  pages: true,
  devtools: {
   enabled: true,

   timeline: {
    enabled: true
   }
  },

  app: {
    head: {
      title: 'HrManagemment',
    },
  },

  runtimeConfig: {
    public: {
      apiUrl: process.env.API_URL,
    },
  },

  nitro: { // todo: 
    experimental: {
      openAPI: true,
    }
  },

  modules: [
   '@primevue/nuxt-module',
   '@nuxtjs/tailwindcss',
   '@vesp/nuxt-fontawesome'
  ],

  fontawesome: {
    icons: {
      solid: ['user'],
      regular: ['user'],
      brands: ['github']
    }
  },

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },

  primevue: {
      options: {
        ripple: true,
        theme: {
            preset: Aura,
            options: {
                darkModeSelector: '.app-dark'
            }
        }
      }
  },
  
  css: [
    '~/assets/shortcuts.css',
    '~/assets/tailwind.css',
    '~/assets/styles.scss',
    'primeicons/primeicons.css',
    /* 'primeflex/primeflex.css', */
  ],

 /*  plugins: [
    '~/plugins/primevue',
    '~/plugins/appState',
  ] */
})