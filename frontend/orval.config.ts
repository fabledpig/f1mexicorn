module.exports = {
  services: {
    output: {
      mode: 'tags-split',
      target: 'services/services.ts',
      schemas: 'services/model',
      client: 'react-query',
      mock: false,
    },

    input: {
      target: './api.json',
    },

    hooks: {
      afterAllFilesWrite: 'npx prettier --write',
    },
  },
};
