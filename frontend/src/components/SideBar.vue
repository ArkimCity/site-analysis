<template>
<div id='sidebar'>
  {{ this.$store.state.selectedBuilding }}
  <br><br><br><br><br>
  <Canvas id="canvas"></Canvas>
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
