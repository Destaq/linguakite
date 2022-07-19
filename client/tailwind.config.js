module.exports = {
  mode: "jit",
  darkMode: "class",
  purge: [
    "./components/**/*.{vue,js}",
    "./pages/**/*.vue",
    "./layouts/**/*.vue",
    "./nuxt.config.js"
  ],
  plugins: [require("daisyui"), require("@tailwindcss/typography")]
};
