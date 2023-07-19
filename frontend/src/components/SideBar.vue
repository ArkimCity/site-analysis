<template>
<div id='sidebar'>
  <!-- <Canvas id="canvas"></Canvas><br> -->
  <!-- 아래는 properties -->
  <br><br><br>
  <div v-if="this.$store.state.selectedBuilding.propertiesData">
    <!-- <div v-for="(value, key) in this.$store.state.selectedBuilding.propertiesData" :key="key">
      {{ key }}:  {{ value }}
    </div> -->
    pnu: {{ this.$store.state.selectedBuilding.propertiesData.A2 }}
    <br>
    주소: {{ this.$store.state.selectedBuilding.propertiesData.A4 }}
    {{ this.$store.state.selectedBuilding.propertiesData.A5 }}
    <br>
    용도: {{ this.$store.state.selectedBuilding.propertiesData.A9 }}
    <br>
    구조: {{ this.$store.state.selectedBuilding.propertiesData.A11 }}
    <br>
  </div>
  <div v-else>
    건물 위에 마우스를 올려주세요
  </div>
</div>
</template>

<script>
// import Canvas from './Canvas.vue'

export default {
  name: 'SideBar',
  components: {
    // Canvas
  }
}
</script>

<style scoped>
#canvas {
    bottom: 0;
}
</style>
