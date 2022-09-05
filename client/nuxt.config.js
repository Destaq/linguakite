export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: "%s | LinguaKite",
    htmlAttrs: {
      lang: "en",
    },
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      {
        hid: "description",
        name: "description",
        content:
          "LinguaKite is an innovative new language-learning platform that teaches you through machine learning and literature.",
      },
      { name: "format-detection", content: "telephone=no" },
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/logo_white.svg" }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [{ src: "~/plugins/axios", mode: "client" }],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/tailwindcss
    "@nuxtjs/tailwindcss",
  ],

  server: {
    port: 3000,
    host: "127.0.0.1", // run on this port so that cookies are set
  },

  

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    "@nuxtjs/axios",
    "@nuxtjs/auth-next",
    ['cookie-universal-nuxt', { alias: 'cookiz' }],
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    baseURL: "http://127.0.0.1:5000/",
    withCredentials: true,
    credentials: true,
    headers: {
      common: {
        "Content-Type": "application/json",
      },
    },
  },

  auth: {
    localStorage: false,
    redirect: {
      login: "/login",
      logout: "/login",
      callback: "/login",
    },
    options: {
      cookie: {
        options: {
          maxAge: 60 * 60 * 24 * 14,
          expires: 14, // and refreshed in 7-day window
        },
      },
    },
    strategies: {
      local: false,
      cookie: {
        token: {
          property: "token",
          required: true,
          type: "Bearer",
          maxAge: 60 * 60 * 24 * 14,
        },
        user: {
          property: "user",
          autoFetch: true,
        },
        endpoints: {
          login: { url: "/api/auth/login", method: "post" },
          logout: { url: "/api/auth/logout", method: "post" },
          user: { url: "/api/auth/user", method: "get" },
        },
        options: {
          maxAge: 60 * 60 * 24 * 14,
          expires: 14, // has no effect
        },
      },
    },
  },
  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},
};
