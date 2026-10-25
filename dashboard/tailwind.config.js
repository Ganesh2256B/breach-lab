/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "#3b82f6",
          foreground: "#eff6ff",
        },
        destructive: {
          DEFAULT: "#ef4444",
          foreground: "#fef2f2",
        },
        accent: {
          DEFAULT: "#1e293b",
          foreground: "#f8fafc",
        },
        card: {
          DEFAULT: "#0f172a",
          foreground: "#f8fafc",
        },
      },
    },
  },
  plugins: [],
}
