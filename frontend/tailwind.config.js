/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        // Ledger palette — cool paper + deep pine ink, not the default
        // warm-cream/terracotta AI look. Green reads as "in the black",
        // rust reads as "in the red" without leaning on stoplight red/green.
        bg: '#F6F7F5',
        surface: '#FFFFFF',
        ink: '#1C2B2D',
        muted: '#64748B',
        subtle: '#E2E5E1',
        accent: '#1F6F5C',
        'accent-soft': '#E4EFEA',
        positive: '#1F8A5F',
        negative: '#A6402A',
        // A second "ink color" for the Breakdown page only — the idea of a
        // ledger using a different colored pen for discretionary vs. fixed
        // spending, rather than inventing an unrelated hue.
        discretionary: '#B98900',
        'discretionary-soft': '#F5EBD2',
      },
      fontFamily: {
        // Space Grotesk: page/section titles — some personality, not a
        // generic system sans.
        display: ['"Space Grotesk"', 'sans-serif'],
        // Inter: nav, labels, body copy — quiet and legible.
        sans: ['Inter', 'sans-serif'],
        // IBM Plex Mono: every dollar amount, percentage, and date in the
        // app. Tabular figures so numbers line up in columns like a real
        // statement — this is the app's signature detail.
        mono: ['"IBM Plex Mono"', 'monospace'],
      },
      borderRadius: {
        DEFAULT: '6px',
      },
    },
  },
  plugins: [],
}
