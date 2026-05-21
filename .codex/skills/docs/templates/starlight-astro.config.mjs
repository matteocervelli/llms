// astro.config.mjs — Starlight template
// Sostituisci {{APP_NAME}}, {{APP_TITLE}}, {{DOMAIN}} con i valori reali
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  // base: '/docs' serve Starlight a {domain}/docs/
  // Rimuovi `base` se questo è un sito docs-only (senza marketing pages)
  base: '/docs',

  integrations: [
    starlight({
      title: '{{APP_TITLE}} Docs',
      defaultLocale: 'it',
      locales: {
        // Italiano — lingua primaria
        it: {
          label: 'Italiano',
          lang: 'it',
        },
        // English — traduzione secondaria
        en: {
          label: 'English',
          lang: 'en',
        },
      },
      sidebar: [
        {
          label: 'Inizia qui',
          translations: { en: 'Start here' },
          items: [
            { slug: 'getting-started' },
          ],
        },
        {
          label: 'Guide',
          translations: { en: 'Guides' },
          autogenerate: { directory: 'guides' },
        },
        {
          label: 'Funzionalità',
          translations: { en: 'Features' },
          autogenerate: { directory: 'features' },
        },
        {
          label: 'Riferimento',
          translations: { en: 'Reference' },
          items: [
            { slug: 'features' },
            { slug: 'faq' },
          ],
        },
      ],
      // Social links (opzionale)
      // social: {
      //   github: 'https://github.com/your-org/{{APP_NAME}}',
      // },
    }),
  ],
});
