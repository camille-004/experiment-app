import js from '@eslint/js';
import vue from 'eslint-plugin-vue';

export default [
  {
    languageOptions: {
      ecmaVersion: 12,
      sourceType: 'module',
      globals: {
        ...js.configs.recommended.languageOptions?.globals,
        ...vue.configs.essential.languageOptions?.globals,
        browser: true,
        es2021: true,
      },
    },
    plugins: {
      vue,
    },
    rules: {
      quotes: ['error', 'single'],
      semi: ['error', 'always'],
    },
  },
];