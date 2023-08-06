const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  outputDir: path.resolve(__dirname, "../docs"),
  publicPath: process.env.NODE_ENV === 'production'
  ? '/site-analysis/'
  : '/',
  transpileDependencies: true
})
