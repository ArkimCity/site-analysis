<template>
  <div>
    <!-- <SideBar id="sidebar"/> -->
    <router-view/>
  </div>
</template>

<script>
// import SideBar from './components/SideBar.vue'

export default {
  components: {
    // SideBar
  }
}
</script>

<style lang="scss">
@import "~vue-maplibre-gl/src/css/maplibre.scss";

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New', monospace;
}

#app {
  width: 100%;
  height: 100vh;
}
</style>
