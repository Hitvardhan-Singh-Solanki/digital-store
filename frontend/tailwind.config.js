/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#e3e8ef",
          100: "#c2cbd9",
          200: "#9aa6c0",
          300: "#6f7da3",
          400: "#4a5a8a",
          500: "#2e3d6e",
          600: "#24315a",
          700: "#1b2547",
          800: "#131a35",
          900: "#0c1125",
        },
        accent: {
          50: "#f4e9f7",
          100: "#e2cde9",
          200: "#cda8d7",
          300: "#b17dc1",
          400: "#9459a9",
          500: "#743b8c",
          600: "#5a2d6e",
          700: "#432152",
          800: "#2e1638",
          900: "#1c0d21",
        },
      },
    },
  },
  plugins: [],
};
