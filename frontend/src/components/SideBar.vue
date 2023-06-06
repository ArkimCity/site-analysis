<template>
<div id='sidebar'>
  <Canvas id="canvas"></Canvas><br>
  {{ this.$store.state.selectedGeo.propertiesData }}
</div>
</template>

<script>
import Canvas from './Canvas.vue'

export default {
  name: 'SideBar',
  components: {
    Canvas
  }
}
</script>

<style>
#canvas {
    bottom: 0;
}
</style>
