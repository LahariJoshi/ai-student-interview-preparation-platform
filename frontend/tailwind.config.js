/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#123E63',
          navy: '#123E63',
          deep: '#0D3557',
          darker: '#09253F',
          light: '#1B5685',
        },
        navy: {
          50: '#F0F5FA',
          100: '#DCE8F2',
          200: '#BCD3E6',
          300: '#8AAEC8',
          400: '#4D82A7',
          500: '#1B5685',
          600: '#123E63',
          700: '#0D3557',
          800: '#09253F',
          900: '#061B2E',
          950: '#030E1A',
        },
        accent: {
          DEFAULT: '#F5A623',
          orange: '#F5A623',
          hover: '#E09212',
          light: '#FFF6E8',
          amber: '#F5A623',
        },
        surface: {
          bg: '#F1F3F6',
          card: '#FFFFFF',
          border: '#E5E9EF',
          muted: '#F8F9FA',
        },
        dashboard: {
          text: '#202B38',
          subtext: '#8993A0',
        },
        brand: {
          50: '#f0f7ff',
          100: '#e0effe',
          500: '#0284c7',
          600: '#0369a1',
          700: '#075985',
        },
      },
      boxShadow: {
        'card': '0 4px 20px -2px rgba(18, 62, 99, 0.05), 0 2px 6px -1px rgba(18, 62, 99, 0.03)',
        'card-hover': '0 12px 30px -4px rgba(18, 62, 99, 0.1), 0 4px 10px -2px rgba(18, 62, 99, 0.05)',
        'shell': '0 25px 60px -15px rgba(13, 53, 87, 0.12), 0 10px 25px -5px rgba(13, 53, 87, 0.08)',
        'navy-card': '0 10px 25px -5px rgba(13, 53, 87, 0.35)',
      },
      borderRadius: {
        'xl': '12px',
        '2xl': '16px',
        '3xl': '24px',
        '4xl': '32px',
      },
    },
  },
  plugins: [],
};
