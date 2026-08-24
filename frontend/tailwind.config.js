/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: '#2c2416',
          light: '#5c5040',
          muted: '#8a7d6b',
        },
        paper: '#f7f5f0',
        paper2: '#faf8f3',
        border: '#e8e0d2',
        accent: {
          DEFAULT: '#8b4513',
          soft: '#f5ebe0',
        },
        olive: {
          DEFAULT: '#556b2f',
          soft: '#e8efe0',
        },
        gold: '#b8860b',
        shu: '#c0392b',
      },
      fontFamily: {
        heading: ['"Noto Serif SC"', '"SimSun"', 'serif'],
        body: ['"PingFang SC"', '"Microsoft YaHei"', 'sans-serif'],
        brush: ['"Ma Shan Zheng"', '"Noto Serif SC"', 'serif'],
      },
      borderRadius: {
        ink: '12px',
      },
      boxShadow: {
        ink: '0 2px 12px rgba(80, 60, 30, 0.06)',
      },
    },
  },
  plugins: [],
}
