import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import astro from 'eslint-plugin-astro';
import jsxA11y from 'eslint-plugin-jsx-a11y';

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  ...astro.configs.recommended,
  {
    files: ['**/*.astro'],
    rules: {
      'astro/no-set-html-directive': 'error'
    }
  },
  {
    plugins: {
      'jsx-a11y': jsxA11y
    },
    rules: {
      ...jsxA11y.configs.recommended.rules
    }
  }
];
