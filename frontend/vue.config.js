
const path = require("path");
module.exports = {
  outputDir: path.resolve(__dirname, "../docs"),
  publicPath: process.env.NODE_ENV === 'production'
    ? '/site-analysis/'
    : '/',
  devServer: {
    // open: process.platform === 'darwin',
    // host: '0.0.0.0',
    // port: 8085, // CHANGE YOUR PORT HERE!
    // hotOnly: false,
    https: true,
  },
}