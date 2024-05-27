import {defineCliConfig} from 'sanity/cli'

export default defineCliConfig({
  api: {
    projectId: 'jv8xevbu',
    dataset: 'production'
  },

  project: {
    basePath: '/studio'
  }
})
