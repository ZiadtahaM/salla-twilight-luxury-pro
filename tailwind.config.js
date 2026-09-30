module.exports = {
    important: false,
    content: [
        "src/views/**/*.twig",
        "src/assets/js/**/*.js",
    ],
    darkMode: 'class',
    theme: {
        container: {
            center: true,
            padding: '10px',
            screens: { '2xl': "1280px" }
        },
        fontFamily: {
            sans: ['var(--font-body)', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
            display: ['var(--font-display)', 'serif'],
        },
        extend: {
            transitionTimingFunction: {
                'elastic': 'cubic-bezier(0.55, 0, 0.1, 1)',
            },
            colors: {
                // Luxury palette — maps to CSS custom properties set in settings
                primary: 'var(--color-primary, #1A1A1A)',
                'primary-d': 'var(--color-primary-dark, #000000)',
                'primary-l': 'var(--color-primary-light, #3A3A3A)',
                'primary-reverse': 'var(--color-primary-reverse, #FFFFFF)',
                // Luxury design tokens
                'luxury-primary': 'var(--luxury-primary, #1A1A1A)',
                'luxury-accent':  'var(--luxury-accent, #D4AF37)',
                'luxury-bg':      'var(--luxury-bg, #FAF9F6)',
                'luxury-surface': 'var(--luxury-surface, #FFFFFF)',
                'luxury-border':  'var(--luxury-border, #E5E2DC)',
                'luxury-text':    'var(--luxury-text, #1C1B1A)',
                'luxury-muted':   'var(--luxury-muted, #6E6B66)',
            },
            spacing: {
                '18': '4.5rem',
                '88': '22rem',
                '128': '32rem',
            },
        },
    },
    plugins: [],
};
