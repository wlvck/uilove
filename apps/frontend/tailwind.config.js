module.exports = {
  content: [
    "./app.vue",
    "./app/**/*.{vue,js,ts}",
    "./components/**/*.{vue,js,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./nuxt.config.{js,ts}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      colors: {
        bg: {
          DEFAULT: "#0a0a0b",
          secondary: "#111113",
          tertiary: "#1a1a1d",
          card: "#141416",
          "card-hover": "#1c1c1f",
        },
        border: {
          DEFAULT: "#27272a",
          hover: "#3f3f46",
        },
        text: {
          primary: "#fafafa",
          secondary: "#a1a1aa",
          tertiary: "#71717a",
        },
        accent: {
          DEFAULT: "#8b5cf6",
          hover: "#7c3aed",
          light: "#a78bfa",
        },
      },
    },
  },
  plugins: [],
};
